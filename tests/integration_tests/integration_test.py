import unittest
import urllib2

class IntegrationTest(unittest.TestCase):
    def test_get(self):
        response = urllib2.urlopen('http://localhost:8000/golden/corn/', data=None)
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the golden corn!')

        response = urllib2.urlopen('http://localhost:8000/metal/silver/food/apple/', data=None)
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the silver apple!')

    def test_post(self):
        response = urllib2.urlopen('http://localhost:8000/golden/corn/', data="")
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets post the golden corn!')

        response = urllib2.urlopen('http://localhost:8000/metal/silver/food/apple/', data="")
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets post the silver apple!')

    def test_redirect(self):
        response = urllib2.urlopen('http://localhost:8000/golden/corn')
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the golden corn!')

        response = urllib2.urlopen('http://localhost:8000/metal/silver/food/apple', data="")
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the silver apple!')

    def test_not_found(self):
        self.assertRaises(urllib2.HTTPError, urllib2.urlopen, 'http://localhost:8000/')

if __name__ == '__main__':
    unittest.main()
