import unittest
from unittest.mock import patch

import redis
from weppy.batteries.redis import RedisExtension

class RedisExtensionTest(unittest.TestCase):
    @patch.object(redis, 'StrictRedis')
    def test(self, mock_method):
        redis_ext = RedisExtension('localhost', 6379)
        mock_method.assert_called_with('localhost', 6379, charset='utf-8',
                                       password=None, decode_responses=True)

if __name__ == '__main__':
    unittest.main()
