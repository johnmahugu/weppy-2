import unittest
from unittest.mock import patch

import pymongo
from weppy.batteries.mongodb import MongoDBExtension

class MongoDBExtensionTest(unittest.TestCase):
    @patch.object(pymongo, 'MongoClient')
    def test_without_password(self, MongoClientMock):
        MongoDBExtension('localhost', 6379, 'db')
        MongoClientMock.assert_called_with('localhost', 6379)

    @patch.object(pymongo, 'MongoClient')
    def test_with_password(self, MongoClientMock):
        client = MongoClientMock.return_value
        MongoDBExtension('localhost', 6379, 'db', username='abc',
                         password='123')
        client.db.authenticate.assert_called_with('abc', '123')

if __name__ == '__main__':
    unittest.main()
