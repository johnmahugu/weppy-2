import unittest
from weppy.test import *
from weppy.handler import *
from weppy.http import *
from weppy.wsgi import *

### Handlers ###

@url('/')
class RootHandler:
    def get(self, req):
        res = HTTPResponse('get, %s' % req.cookies.get('method', ''))
        res.set_cookie('method', 'get')
        return res

    def post(self, req):
        res = HTTPResponse('post, %s' % req.cookies.get('method', ''))
        res.set_cookie('method', 'post')
        return res

    def put(self, req):
        res = HTTPResponse('put, %s' % req.cookies.get('method', ''))
        res.set_cookie('method', 'put')
        return res

    def delete(self, req):
        res = HTTPResponse('delete, %s' % req.cookies.get('method', ''))
        res.set_cookie('method', 'delete')
        return res

### Tests ###

class ClientTest(unittest.TestCase):
    def setUp(self):
        app = WSGIApplication(True)
        app.add_handler(RootHandler)
        self.client = Client(app)

    def test_get(self):
        res = self.client.get('/')
        self.assertEqual(res.text, 'get, ')
        res = self.client.get('/')
        self.assertEqual(res.text, 'get, get')

    def test_post(self):
        res = self.client.post('/')
        self.assertEqual(res.text, 'post, ')
        res = self.client.get('/')
        self.assertEqual(res.text, 'get, post')

    def test_put(self):
        res = self.client.put('/')
        self.assertEqual(res.text, 'put, ')
        res = self.client.get('/')
        self.assertEqual(res.text, 'get, put')

    def test_delete(self):
        res = self.client.delete('/')
        self.assertEqual(res.text, 'delete, ')
        res = self.client.get('/')
        self.assertEqual(res.text, 'get, delete')

    def test_head(self):
        res = self.client.head('/')
        self.assertEqual(res.text, '')
        res = self.client.get('/')
        self.assertEqual(res.text, 'get, get')

if __name__ == '__main__':
    unittest.main()
