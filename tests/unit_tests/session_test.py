import json
import redis
import unittest
from unittest.mock import patch

from weppy.batteries.session.extension import RedisSessionExtension
from weppy.batteries.session.decorator import login_required
from weppy.handler import RequestHandler
from weppy.http import *

class StrictRedisMock:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, key):
        if key == 'true':
            return json.dumps({
                'created_at': 'now',
                'csrf_token': 'token',
                'user': None,
                'data': {'abc': '123'}
            })
        return None

    def set(self, key, value):
        pass

class RequestHandlerA(RequestHandler):
    @login_required('http://login.com')
    def post(self, request):
        return HTTPResponse('get')

class SessionTest(unittest.TestCase):
    @patch.object(redis, 'StrictRedis', StrictRedisMock)
    def setUp(self):
        self.ext = RedisSessionExtension('cookie', 'localhost', 6379)

    def test_session(self):
        req = HTTPRequest.post(params={'csrf_token': 'token'},
                               headers={'HTTP_COOKIE': 'cookie=true'})
        self.ext.process_request(req)
        self.assertEqual(self.ext.session_id, 'true')
        self.assertEqual(req.session['abc'], '123')
        req.session.login('id')
        self.assertEqual(req.session.user, 'id')
        req.session.logout()
        self.assertEqual(req.session.user, None)
        res = HTTPResponse()
        self.ext.process_response(req, res)
        self.assertFalse('Set-Cookie' in dict(res.headerlist))

    def test_csrf(self):
        req = HTTPRequest.post(params={'csrf_token': 'invalid'},
                               headers={'HTTP_COOKIE': 'cookie=true'})
        self.assertRaises(HTTPForbidden, self.ext.process_request, req)

    def test_set_cookie(self):
        req = HTTPRequest.get(headers={'HTTP_COOKIE': 'cookie=false'})
        self.ext.process_request(req)
        self.assertNotEqual(self.ext.session_id, 'false')
        res = HTTPResponse()
        self.ext.process_response(req, res)
        self.assertTrue(
            dict(res.headerlist)['Set-Cookie'].startswith('cookie=')
        )

    def test_login_required(self):
        req = HTTPRequest.post(params={'csrf_token': 'token'},
                               headers={'HTTP_COOKIE': 'cookie=true'})
        self.ext.process_request(req)
        req.session.login('id')
        res = RequestHandlerA('/')(req)
        self.assertEqual(res.status, '200 OK')

        req.session.logout()
        res = RequestHandlerA('/')(req)
        self.assertEqual(res.status, '302 Found')

if __name__ == '__main__':
    unittest.main()
