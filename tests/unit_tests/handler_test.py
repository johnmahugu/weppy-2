import unittest

from weppy.handler import RequestHandler, ErrorHandler, url
from weppy.http import *

@url('/', 'handler')
class RequestHandlerA:
    def get(self, request):
        return HTTPResponse('get')

    def post(self, request):
        return HTTPResponse('post')

class ErrorHandlerA(ErrorHandler):
    def error404(self, http_error):
        return HTTPResponse('404', status=http_error.status)

    def error5xx(self, http_error):
        return HTTPResponse('5xx', status=http_error.status)

    def error(self, http_error):
        return HTTPResponse('error', status=http_error.status)

class RequestHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = RequestHandlerA

    def test_init(self):
        self.assertEqual(self.handler.url_pattern, '/')
        self.assertEqual(self.handler.handler_name, 'handler')

    def test_call(self):
        res = self.handler(HTTPRequest.get())
        self.assertEqual(res.text, 'get')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = self.handler(HTTPRequest.post())
        self.assertEqual(res.text, 'post')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = self.handler(HTTPRequest.head())
        self.assertEqual(res.text, '')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        self.assertRaises(HTTPMethodNotAllowed, self.handler, HTTPRequest.put())

class ErrorHandlerTest(unittest.TestCase):
    def test_call(self):
        handler = ErrorHandlerA()

        res = handler(HTTPMethodNotAllowed())
        self.assertEqual(res.status, '405 Method Not Allowed')
        self.assertEqual(res.text, 'error')

        res = handler(HTTPNotFound())
        self.assertEqual(res.status, '404 Not Found')
        self.assertEqual(res.text, '404')

        res = handler(HTTPInternalServerError())
        self.assertEqual(res.status, '500 Internal Server Error')
        self.assertEqual(res.text, '5xx')

class urlDecoratorTest(unittest.TestCase):
    def test_decorator(self):
        self.assertTrue(isinstance(RequestHandlerA, RequestHandler))

        res = RequestHandlerA(HTTPRequest.get())
        self.assertEqual(res.text, 'get')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = RequestHandlerA(HTTPRequest.post())
        self.assertEqual(res.text, 'post')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = RequestHandlerA(HTTPRequest.head())
        self.assertEqual(res.text, '')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        self.assertRaises(HTTPMethodNotAllowed, RequestHandlerA,
                          HTTPRequest.put())

if __name__ == '__main__':
    unittest.main()
