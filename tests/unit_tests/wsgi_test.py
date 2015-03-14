import os
import unittest
from weppy.handler import *
from weppy.http import *
from weppy.wsgi import *

### Handlers ###

@url('/')
class RootHandler:
    def get(self, req):
        return HTTPResponse('get')

    def post(self, req):
        return HTTPResponse('post')

@url('/arg/_/')
class ArgHandler:
    def get(self, req, arg):
        return HTTPResponse('get %s' % arg)

    def post(self, req, arg):
        return HTTPResponse('post %s' % arg)

@url('/error/')
class ErrorHandler:
    def get(self, req):
        return HTTPResponse('%s' % 1 / 0)

### Tests ###

class WSGIApplicationTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(False)
        self.app.add_handler(RootHandler)
        self.app.add_handler(ArgHandler)
        self.app.add_handler(ErrorHandler)

    def test_get(self):
        req = HTTPRequest.get(path_info='/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'get')

        req = HTTPRequest.get(path_info='/arg/gold/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'get gold')

    def test_post(self):
        req = HTTPRequest.post(path_info='/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'post')

        req = HTTPRequest.post(path_info='/arg/gold/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'post gold')

    def test_redirect(self):
        req = HTTPRequest.get(path_info='')
        res = self.app.handle_request(req)
        self.assertEqual(res.status, '302 Found')

        req = HTTPRequest.get(path_info='/arg/gold')
        res = self.app.handle_request(req)
        self.assertEqual(res.status, '302 Found')

    def test_not_found(self):
        req = HTTPRequest.get(path_info='/gold/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'Error 404')
        self.assertEqual(res.status, '404 Not Found')

    def test_internal_server_error(self):
        req = HTTPRequest.get(path_info='/error/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'Error 500')
        self.assertEqual(res.status, '500 Internal Server Error')

    def test_method_not_allowed(self):
        req = HTTPRequest.put(path_info='/')
        res = self.app.handle_request(req)
        self.assertEqual(res.text, 'Error 405')
        self.assertEqual(res.status, '405 Method Not Allowed')

if __name__ == '__main__':
    unittest.main()
