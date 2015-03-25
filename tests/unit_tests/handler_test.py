import unittest
from weppy.handler import *
from weppy.http import *

### Handlers ###

@url('/')
class RootHandler:
    def get(self, req):
        return HTTPResponse('get')

    def post(self, req):
        return HTTPResponse('post')

@url('/one/_/')
class OneArgHandler:
    def get(self, req, one):
        return HTTPResponse('%s' % one)

@url('/two/_/_/')
class TwoArgsHandler:
    def get(self, req, one, two):
        return HTTPResponse('%s, %s' % (one, two))

@url('/str/')
class StrHandler:
    def get(self, req):
        return 'get'

    def post(self, req):
        return 'post'

### Tests ###

class HandlerTest(unittest.TestCase):
    def test_url_regex(self):
        self.assertEqual(RootHandler._url_regex.pattern, r'^\/$')
        self.assertEqual(OneArgHandler._url_regex.pattern, r'^\/one\/([^/]+)\/$')
        self.assertEqual(TwoArgsHandler._url_regex.pattern, r'^\/two\/([^/]+)\/([^/]+)\/$')

    def test_get(self):
        res = RootHandler(HTTPRequest.get())
        self.assertEqual(res.text, 'get')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = OneArgHandler(HTTPRequest.get(), 'one')
        self.assertEqual(res.text, 'one')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = TwoArgsHandler(HTTPRequest.get(), 'one', 'two')
        self.assertEqual(res.text, 'one, two')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = StrHandler(HTTPRequest.get())
        self.assertEqual(res.text, 'get')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

    def test_post(self):
        res = RootHandler(HTTPRequest.post())
        self.assertEqual(res.text, 'post')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = StrHandler(HTTPRequest.post())
        self.assertEqual(res.text, 'post')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

    def test_head(self):
        res = RootHandler(HTTPRequest.head())
        self.assertEqual(res.text, '')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = OneArgHandler(HTTPRequest.head(), 'one')
        self.assertEqual(res.text, '')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = TwoArgsHandler(HTTPRequest.head(), 'one', 'two')
        self.assertEqual(res.text, '')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

        res = StrHandler(HTTPRequest.head())
        self.assertEqual(res.text, '')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.content_type, 'text/html')
        self.assertEqual(res.charset, 'UTF-8')

    def test_method_not_allowed(self):
        self.assertRaises(HTTPMethodNotAllowed, RootHandler, HTTPRequest.put())
        self.assertRaises(HTTPMethodNotAllowed, RootHandler, HTTPRequest.delete())

class urlTest(unittest.TestCase):
    def test_decorator(self):
        self.assertTrue(isinstance(RootHandler, Handler))

if __name__ == '__main__':
    unittest.main()
