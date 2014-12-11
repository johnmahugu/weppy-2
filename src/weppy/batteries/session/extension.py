import json
from datetime import datetime

import redis
from weppy.extension import Extension
from weppy.http import *
from weppy.util import random_string

class RedisSession(dict):
    """
    User session data dictionary saved in a Redis server.
    """

    def __init__(self, redis, session_id, values):
        """
        redis -- connection to the Redis server.
        session_id -- str that specifies the session id.
        values -- str that represents values of the session.
        """
        super().__init__()
        self._redis = redis
        self._session_id = session_id
        session = json.loads(values)
        self._created_at = session.get('created_at', str(datetime.now()))
        self._csrf_token = session.get('csrf_token', random_string(64))
        self._user = session.get('user', None)
        if session:
            self.update(session['data'])
        else:
            self.save()

    # Properties to access session attributes.
    created_at = property(lambda self: self._created_at)
    csrf_token = property(lambda self: self._csrf_token)
    user = property(lambda self: self._user)

    def login(self, user):
        """
        Sets the user identification of the session.

        user -- user identification value.
        """
        self._user = user
        self.save()

    def logout(self):
        """
        Unset the user identification of the session.
        """
        self._user = None
        self.save()

    def save(self):
        """
        Saves the data of the session in the Redis server.
        """
        session = {
            'created_at': self._created_at,
            'csrf_token': self._csrf_token,
            'user': self._user,
            'data': self
        }
        self._redis.set(self._session_id,
                        json.dumps(session, separators=(',', ':')))

class RedisSessionExtension(Extension):
    def __init__(self, cookie_name, host, port, password=None, charset='utf-8',
                 cookie_max_age=None, check_csrf_token=True,
                 attr_name='session'):
        """
        cookie_name -- str that specifies the name of the cookie that stores
                       the session id.
        host -- str that specifies the host of the Redis server.
        port -- int that specifies the port of the Redis server.
        password -- str that specifies the password of the Redis server. None by
                    default.
        charset -- str that specifies the charset encoding of the Redis server.
                   'utf-8' by default.
        cookie_max_age -- int that specifies the 'Max-Age' attribute of the
                          cookie in seconds. A None value sets a session cookie.
                          None by default.
        check_csrf_token -- bool that specifies if the CSRF token is verified.
                            True by default.
        attr_name -- str that specifies the name of the attribute of the request
                     object in which the session is set. 'session' by default.
        """
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.redis = redis.StrictRedis(host, port, password=password,
                                       charset=charset, decode_responses=True)
        self.check_csrf_token = check_csrf_token
        self.attr_name = attr_name

    def process_request(self, request):
        """
        Sets a session dictionary backed by a Redis server in the request
        object.

        request -- HTTPRequest instance.
        """
        self.session_id = request.cookies.get(self.cookie_name, None)
        values = self.redis.get(self.session_id) if self.session_id else None
        if self.session_id is None or values is None:
            self.session_id = random_string(64)
            values = values or '{}'
        session = RedisSession(self.redis, self.session_id, values)
        setattr(request, self.attr_name, session)
        if request.method == 'POST':
            token = session.csrf_token
            post_token = request.POST.get('csrf_token', None)
            if token != post_token and self.check_csrf_token:
                raise HTTPForbidden()

    def process_response(self, request, response):
        """
        Sets the session id in the cookie.

        request -- HTTPRequest instance.
        response -- HTTPResponse instance.
        """
        session_id = request.cookies.get(self.cookie_name, None)
        if session_id is None or self.session_id != session_id:
            response.set_cookie(self.cookie_name, self.session_id,
                                self.cookie_max_age)
