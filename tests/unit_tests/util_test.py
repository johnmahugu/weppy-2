import unittest

from weppy.util import random_string

class UtilTest(unittest.TestCase):
    def test_random_string(self):
        self.assertEqual(len(random_string(0)), 0)
        self.assertEqual(len(random_string(64)), 64)
        self.assertEqual(random_string(3, 'a'), 'aaa')

if __name__ == '__main__':
    unittest.main()
