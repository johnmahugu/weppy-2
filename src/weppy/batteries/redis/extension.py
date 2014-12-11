import redis
from weppy.extension import Extension

class RedisExtension(Extension):
    """
    Sets a connection to a Redis server in the app object.
    """

    def __init__(self, host, port, password=None, charset='utf-8',
                 attr_name='redis'):
        """
        host -- str that specifies the hostname or IP address of the server.
        port -- int that specifies the port number on which to connect.
        password -- str that specifies the password of the server. None by
                    default.
        charset -- str that specifies the charset encoding of the server.
                   'utf-8' by default.
        attr_name -- str that specifies the name of the attribute of the app
                     object in which the connection is set. 'redis' by default.
        """
        self.attr_name = attr_name
        self.redis = redis.StrictRedis(host, port, password=password,
                                       charset=charset, decode_responses=True)

    def __call__(self, app):
        """
        Sets the connection in the app object.

        app -- WSGIApplication instance.
        """
        setattr(app, self.attr_name, self.redis)
