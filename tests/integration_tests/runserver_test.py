import unittest
import urllib.request
from urllib.error import HTTPError

class IntegrationTest(unittest.TestCase):
    def test_get(self):
        response = urllib.request.urlopen('http://localhost:8000/wall/')
        text = response.read()
        self.assertEqual(text.decode('utf-8'),
                         '["Hello, World!", "Ola, Mundo!"]')

    def test_append_slash(self):
        response = urllib.request.urlopen('http://localhost:8000/wall')
        text = response.read()
        self.assertEqual(text.decode('utf-8'),
                         '["Hello, World!", "Ola, Mundo!"]')

    def test_404(self):
        self.assertRaises(HTTPError, urllib.request.urlopen,
                          'http://localhost:8000/')

if __name__ == '__main__':
    unittest.main()
