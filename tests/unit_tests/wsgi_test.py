import os
import unittest

from weppy.extension import Extension
from weppy.handler import ErrorHandler, url
from weppy.http import *
from weppy.wsgi import WSGIApplication

@url('/test/', 'handler_a')
class RequestHandlerA:
    def get(self, request):
        return HTTPResponse('get')

    def post(self, request):
        return HTTPResponse('post')

@url('/test/_/', 'handler_b')
class RequestHandlerB:
    def get(self, request, arg):
        return HTTPResponse('get %s' % arg)

    def post(self, request, arg):
        return HTTPResponse('post %s' % arg)

@url('/error/', 'handler_c')
class RequestHandlerC:
    def get(self, request):
        return HTTPResponse('%s' % 1 / 0)

class ErrorHandlerA(ErrorHandler):
    def error404(self, http_error):
        return HTTPResponse('404', status=http_error.status)

    def error5xx(self, http_error):
        return HTTPResponse('5xx', status=http_error.status)

    def error(self, http_error):
        return HTTPResponse('error', status=http_error.status)

class ExtensionA(Extension):
    def __call__(self, app):
        setattr(app, 'one', 1)

    def process_request(self, request):
        setattr(request, 'two', 2)

    def process_response(self, request, response):
        setattr(request, 'three', 3)

class WSGIApplicationTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(False, extensions=[ExtensionA()])
        self.app.add_request_handler(RequestHandlerA)
        self.app.add_request_handler(RequestHandlerB)
        self.app.add_request_handler(RequestHandlerC)
        self.app.set_error_handler(ErrorHandlerA())

        static_root = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'resources', 'static')
        self.debug_app = WSGIApplication(True, static_root=static_root)

    def test_init(self):
        self.assertEqual(self.app.one, 1)
        self.assertEqual(len(self.app._extensions), 1)
        self.assertEqual(len(self.app._routes), 3)
        self.assertEqual(len(self.app._reverse_routes), 3)
        self.assertTrue(isinstance(self.app._error_handler, ErrorHandlerA))

        self.assertEqual(len(self.debug_app._extensions), 0)
        self.assertEqual(len(self.debug_app._routes), 0)
        self.assertEqual(len(self.debug_app._reverse_routes), 0)
        self.assertTrue(isinstance(self.debug_app._error_handler, ErrorHandler))

    def test_debug(self):
        self.assertFalse(self.app.debug)
        self.assertTrue(self.debug_app.debug)

    def test_add_request_handler(self):
        app = WSGIApplication(False)
        app.add_request_handler(RequestHandlerA)
        self.assertEqual(RequestHandlerA.app, app)
        self.assertEqual(len(app._routes), 1)
        self.assertEqual(len(app._reverse_routes), 1)

    def test_set_error_handler(self):
        error_handler = ErrorHandlerA()
        self.debug_app.set_error_handler(error_handler)
        self.assertEqual(self.debug_app._error_handler, error_handler)
        self.assertEqual(error_handler.app, self.debug_app)

    def test_reverse(self):
        self.assertEqual(self.app.reverse('handler_a'), '/test/')
        self.assertEqual(self.app.reverse('handler_b', 'abc'), '/test/abc/')
        self.assertEqual(self.app.reverse('handler_c'), '/error/')
        self.assertRaises(TypeError, self.app.reverse, 'handler_a', 'abc')
        self.assertRaises(TypeError, self.app.reverse, 'handler_b')
        self.assertRaises(ValueError, self.app.reverse, 'handler_d')

    def test_controller(self):
        req = HTTPRequest.get(path_info='/test/')
        res = self.app._controller(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'get')

        req = HTTPRequest.post(path_info='/test/')
        res = self.app._controller(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'post')

        req = HTTPRequest.get(path_info='/test/abc/')
        res = self.app._controller(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'get abc')

        req = HTTPRequest.post(path_info='/test/abc/')
        res = self.app._controller(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'post abc')

        req = HTTPRequest.get(path_info='/test')
        res = self.app._controller(req)
        self.assertEqual(res.status, '302 Found')

        req = HTTPRequest.get(path_info='/abc/')
        self.assertRaises(HTTPNotFound, self.app._controller, req)

        req = HTTPRequest.get(path_info='/error/')
        self.assertRaises(Exception, self.app._controller, req)

        req = HTTPRequest.get(path_info='/static/image.png')
        self.assertRaises(HTTPNotFound, self.app._controller, req)

        file = open('%s/image.png' % self.debug_app._static_root, 'rb')
        req = HTTPRequest.get(path_info='/static/image.png')
        res = self.debug_app._controller(req)
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, file.read())
        self.assertEqual(res.content_type, 'image/png')
        self.assertEqual(res.charset, None)
        file.close()

        req = HTTPRequest.get(path_info='/static/image.jpg')
        self.assertRaises(HTTPNotFound, self.debug_app._controller, req)

    def test_handle_request(self):
        req = HTTPRequest.get(path_info='/test/')
        res = self.app._handle_request(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'get')

        req = HTTPRequest.post(path_info='/test/')
        res = self.app._handle_request(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'post')

        req = HTTPRequest.get(path_info='/test/abc/')
        res = self.app._handle_request(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'get abc')

        req = HTTPRequest.post(path_info='/test/abc/')
        res = self.app._handle_request(req)
        self.assertEqual(req.two, 2)
        self.assertEqual(req.three, 3)
        self.assertEqual(res.text, 'post abc')

        req = HTTPRequest.get(path_info='/test')
        res = self.app._handle_request(req)
        self.assertEqual(res.status, '302 Found')

        req = HTTPRequest.get(path_info='/abc/')
        res = self.app._handle_request(req)
        self.assertEqual(res.text, '404')
        self.assertEqual(res.status, '404 Not Found')

        req = HTTPRequest.get(path_info='/error/')
        res = self.app._handle_request(req)
        self.assertEqual(res.text, '5xx')
        self.assertEqual(res.status, '500 Internal Server Error')

        req = HTTPRequest.get(path_info='/static/image.png')
        res = self.app._handle_request(req)
        self.assertEqual(res.status, '404 Not Found')

        file = open('%s/image.png' % self.debug_app._static_root, 'rb')
        req = HTTPRequest.get(path_info='/static/image.png')
        res = self.debug_app._handle_request(req)
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, file.read())
        self.assertEqual(res.content_type, 'image/png')
        self.assertEqual(res.charset, None)
        file.close()

        req = HTTPRequest.get(path_info='/static/image.jpg')
        res = self.debug_app._handle_request(req)
        self.assertEqual(res.status, '404 Not Found')

if __name__ == '__main__':
    unittest.main()
