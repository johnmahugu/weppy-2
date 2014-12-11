import cgi
import unittest

from weppy.http import *

class HTTPRequestTest(unittest.TestCase):
    def test_method(self):
        req = HTTPRequest.get()
        self.assertEqual(req.method, 'GET')

        req = HTTPRequest.head()
        self.assertEqual(req.method, 'HEAD')

        req = HTTPRequest.post()
        self.assertEqual(req.method, 'POST')

        req = HTTPRequest.put()
        self.assertEqual(req.method, 'PUT')

        req = HTTPRequest.delete()
        self.assertEqual(req.method, 'DELETE')

    def test_http_version(self):
        req = HTTPRequest.get()
        self.assertEqual(req.http_version, 'HTTP/1.1')

        req = HTTPRequest.get(http_version='HTTP/1.0')
        self.assertEqual(req.http_version, 'HTTP/1.0')

    def test_charset(self):
        req = HTTPRequest.get()
        self.assertEqual(req.charset, 'UTF-8')

    def test_host_name(self):
        req = HTTPRequest.get(server_name='localhost', server_port=8000)
        self.assertEqual(req.host_name, 'http://localhost:8000')

        req = HTTPRequest.get(server_name='uol.com.br', server_port=80)
        self.assertEqual(req.host_name, 'http://uol.com.br')

    def test_host_port(self):
        req = HTTPRequest.get(server_port=80)
        self.assertEqual(req.host_port, 80)

    def test_host(self):
        req = HTTPRequest.get(server_name='localhost', server_port=8000)
        self.assertEqual(req.host, 'localhost:8000')

        req = HTTPRequest.get(server_name='uol.com.br', server_port=80)
        self.assertEqual(req.host, 'uol.com.br:80')

    def test_path(self):
        req = HTTPRequest.get(script_name='', path_info='/post/delete')
        self.assertEqual(req.path, '/post/delete')

        req = HTTPRequest.get(script_name='/post/delete', path_info='')
        self.assertEqual(req.path, '/post/delete')

        req = HTTPRequest.get(script_name='/wiki', path_info='/post/delete')
        self.assertEqual(req.path, '/wiki/post/delete')

    def test_query_string(self):
        req = HTTPRequest.get(query_string='abc=def&123=456')
        self.assertEqual(req.query_string, 'abc=def&123=456')

    def test_url(self):
        req = HTTPRequest.get(server_name='uol.com.br', server_port=80,
                              script_name='/wiki', path_info='/post/delete',
                              query_string='abc=def', url_scheme='https')
        self.assertEqual(req.url,
                         'https://uol.com.br:80/wiki/post/delete?abc=def')

    def test_body(self):
        req = HTTPRequest.post()
        self.assertEqual(req.body, b'')

        req = HTTPRequest.post(params={'abc': 'def'})
        self.assertEqual(req.body, b'abc=def')

        req = HTTPRequest.post(params={'abc': 'def', '123': '456'})
        self.assertIn(b'123=456', req.body)
        self.assertIn(b'abc=def', req.body)

    def test_text(self):
        req = HTTPRequest.post()
        self.assertEqual(req.text, '')

        req = HTTPRequest.post(params={'abc': 'def'})
        self.assertEqual(req.text, 'abc=def')

        req = HTTPRequest.post(params={'abc': 'def', '123': '456'})
        self.assertIn('123=456', req.text)
        self.assertIn('abc=def', req.text)

    def test_GET(self):
        req = HTTPRequest.get(query_string='abc=def&123=456&abc=ghi')
        self.assertEqual(req.GET.getall('abc'), ['def', 'ghi'])
        self.assertEqual(req.GET.getall('123'), ['456'])

    def test_POST(self):
        req = HTTPRequest.post(params={'abc': 'def', '123': '456'})
        self.assertEqual(req.POST.getall('abc'), ['def'])
        self.assertEqual(req.POST.getall('123'), ['456'])

        req = HTTPRequest.post(params={'file': ('filename', b'content')})
        self.assertTrue(isinstance(req.POST['file'], cgi.FieldStorage))

    def test_headers(self):
        req = HTTPRequest.get(
            headers={
                'HTTP_CONNECTION': 'keep-alive',
                'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                                   '10_6_8) AppleWebKit/537.36 (KHTML, '
                                   'like Gecko)',
                'HTTP_ACCEPT': 'text/html,application/xhtml+xml,'
                               'application/xml;q=0.9,image/webp,*/*;q=0.8',
                'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch',
                'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.8,de;q=0.6,es;q=0.4,'
                                        'fr;q=0.2,it;q=0.2,pt;q=0.2,'
            }
        )
        self.assertEqual(req.headers['Connection'], 'keep-alive')
        self.assertEqual(req.headers['User-Agent'], 'Mozilla/5.0 (Macintosh; '
                         'Intel Mac OS X 10_6_8) AppleWebKit/537.36 '
                         '(KHTML, like Gecko)')
        self.assertEqual(req.headers['Accept'], 'text/html,application/xhtml+'
                         'xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        self.assertEqual(req.headers['Accept-Encoding'], 'gzip,deflate,sdch')
        self.assertEqual(req.headers['Accept-Language'], 'en-US,en;q=0.8,de;'
                         'q=0.6,es;q=0.4,fr;q=0.2,it;q=0.2,pt;q=0.2,')

        req = HTTPRequest.post()
        self.assertEqual(req.headers['Content-Type'],
                         'application/x-www-form-urlencoded')

        req = HTTPRequest.post(params={'file': ('filename', b'content')})
        self.assertIn('multipart/form-data; boundary=',
                      req.headers['Content-Type'])

    def test_cookies(self):
        req = HTTPRequest.get(headers={'HTTP_COOKIE': 'abc=def; 123=456'})
        self.assertEqual(req.cookies['abc'], 'def')
        self.assertEqual(req.cookies['123'], '456')

    def test_accept(self):
        req = HTTPRequest.get(
            headers={
                'HTTP_ACCEPT': 'text/html,application/xhtml+xml,'
                               'application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
        )
        self.assertEqual(req.accept, ['text/html', 'application/xhtml+xml',
                                      'image/webp', 'application/xml', '*/*'])

    def test_accept_charset(self):
        req = HTTPRequest.get(
            headers={'HTTP_ACCEPT_CHARSET': 'iso-8859-5,unicode-1-1;q=0.8'}
        )
        self.assertEqual(req.accept_charset, ['iso-8859-5', 'iso-8859-1',
                                              'unicode-1-1'])

    def test_accept_encoding(self):
        req = HTTPRequest.get(
            headers={'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch'}
        )
        self.assertEqual(req.accept_encoding, ['gzip', 'deflate', 'sdch'])

    def test_accept_language(self):
        req = HTTPRequest.get(
            headers={
                'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.8,de;q=0.6,es;q=0.4,'
                                        'fr;q=0.2,it;q=0.2,pt;q=0.2,'
            }
        )
        self.assertEqual(req.accept_language, ['en-US', 'en', 'de', 'es', 'fr',
                                               'it', 'pt'])

class HTTPResponseTest(unittest.TestCase):
    def test_body(self):
        res = HTTPResponse(body='abc123')
        self.assertEqual(res.body, b'abc123')

    def test_text(self):
        res = HTTPResponse(body='abc123')
        self.assertEqual(res.text, 'abc123')

    def test_content_type(self):
        res = HTTPResponse(content_type='text/plain')
        self.assertEqual(res.content_type, 'text/plain')

        res = HTTPResponse(content_type='image/jpeg')
        self.assertEqual(res.content_type, 'image/jpeg')

    def test_status(self):
        res = HTTPResponse(status=200)
        self.assertEqual(res.status, '200 OK')

        res = HTTPResponse(status=404)
        self.assertEqual(res.status, '404 Not Found')

    def test_charset(self):
        res = HTTPResponse(charset='utf-8')
        self.assertEqual(res.charset, 'utf-8')

        res = HTTPResponse(charset='latin-1')
        self.assertEqual(res.charset, 'latin-1')

    def test_headerlist(self):
        res = HTTPResponse(headerlist=[('Set-Cookie', 'abc=def; 123=456'),
                                       ('Cache-Control', 'max-age=60')])
        self.assertEqual(res.headerlist, [('Set-Cookie', 'abc=def; 123=456'),
                                          ('Cache-Control', 'max-age=60'),
                                          ('Content-Length', '0')])

    def test_cache_expires(self):
        res = HTTPResponse()
        res.cache_expires(5)
        self.assertIn(('Cache-Control', 'max-age=5'), res.headerlist)

    def test_set_cookie(self):
        res = HTTPResponse()
        res.set_cookie('abc', 'def')
        self.assertIn(('Set-Cookie', 'abc=def; Path=/'), res.headerlist)

    def test_unset_cookie(self):
        res = HTTPResponse()
        res.set_cookie('abc', 'def')
        res.set_cookie('123', '456')
        res.unset_cookie('abc')
        self.assertIn(('Set-Cookie', '123=456; Path=/'), res.headerlist)

    def test_delete_cookie(self):
        res = HTTPResponse()
        res.delete_cookie('abc')
        self.assertTrue(
            dict(res.headerlist)['Set-Cookie'].startswith(
                'abc=; Max-Age=0; Path=/'
            )
        )

class HTTPRedirectTest(unittest.TestCase):
    def test(self):
        res = HTTPRedirect('http://www.google.com')
        self.assertEqual(res.status, '302 Found')
        self.assertIn(('Location', 'http://www.google.com'), res.headerlist)

        res = HTTPRedirect('http://www.google.com', True)
        self.assertEqual(res.status, '301 Moved Permanently')
        self.assertIn(('Location', 'http://www.google.com'), res.headerlist)

class HTTPErrorTest(unittest.TestCase):
    def test(self):
        error = HTTPError(404)
        self.assertEqual(error.status, 404)
        self.assertEqual(str(error), 'Error 404')

class HTTPForbiddenTest(unittest.TestCase):
    def test(self):
        error = HTTPForbidden()
        self.assertEqual(error.status, 403)
        self.assertEqual(str(error), 'Error 403')

class HTTPNotFoundTest(unittest.TestCase):
    def test(self):
        error = HTTPNotFound()
        self.assertEqual(error.status, 404)
        self.assertEqual(str(error), 'Error 404')

class HTTPMethodNotAllowedTest(unittest.TestCase):
    def test(self):
        error = HTTPMethodNotAllowed()
        self.assertEqual(error.status, 405)
        self.assertEqual(str(error), 'Error 405')

class HTTPInternalServerErrorTest(unittest.TestCase):
    def test(self):
        error = HTTPInternalServerError()
        self.assertEqual(error.status, 500)
        self.assertEqual(str(error), 'Error 500')

if __name__ == '__main__':
    unittest.main()
