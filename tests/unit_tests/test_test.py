import unittest

from weppy.batteries.test import Client
from weppy.handler import url
from weppy.http import *
from weppy.wsgi import WSGIApplication

@url('/a/', 'handler_a')
class RequestHandlerA:
    def get(self, request):
        return HTTPResponse('get')

    def post(self, request):
        return HTTPResponse('post')

    def put(self, request):
        return HTTPResponse('put')

    def delete(self, request):
        return HTTPResponse('delete')

@url('/b/', 'handler_b')
class RequestHandlerB:
    def post(self, request):
        res = HTTPResponse(request.cookies.get('content', ''))
        res.set_cookie('content', request.POST.get('content', ''))
        return res

class ClientTest(unittest.TestCase):
    def setUp(self):
        app = WSGIApplication(True)
        app.add_request_handler(RequestHandlerA)
        app.add_request_handler(RequestHandlerB)
        self.client = Client(app)

    def test_get(self):
        res = self.client.get('/a/')
        self.assertEqual(res.text, 'get')

    def test_post(self):
        res = self.client.post('/a/')
        self.assertEqual(res.text, 'post')

    def test_put(self):
        res = self.client.put('/a/')
        self.assertEqual(res.text, 'put')

    def test_delete(self):
        res = self.client.delete('/a/')
        self.assertEqual(res.text, 'delete')

    def test_head(self):
        res = self.client.head('/a/')
        self.assertEqual(res.text, '')

    def test_cookie_processing(self):
        res = self.client.post('/b/', {'content': 'abc'})
        self.assertEqual(res.text, '')

        res = self.client.post('/b/')
        self.assertEqual(res.text, 'abc')

if __name__ == '__main__':
    unittest.main()
