import logging
import os
import unittest

from weppy.batteries.logger.extension import StreamLoggerExtension, \
        FileLoggerExtension
from weppy.wsgi import WSGIApplication

class StreamLoggerExtensionTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(
            False,
            extensions=[
                StreamLoggerExtension('stream', '::: %(message)s :::',
                                      attr_name='stream_logger')
            ]
        )
        self.debug_app = WSGIApplication(
            True,
            extensions=[
                StreamLoggerExtension('debug_stream', '!!! %(message)s !!!',
                                      attr_name='stream_logger')
            ]
        )

    def test_app(self):
        self.assertTrue(isinstance(self.app.stream_logger, logging.Logger))
        self.assertTrue(isinstance(self.app.stream_logger.handlers[0],
                                   logging.StreamHandler))
        self.assertEqual(self.app.stream_logger.level, logging.INFO)

    def test_debug_app(self):
        self.assertTrue(isinstance(self.debug_app.stream_logger,
                                   logging.Logger))
        self.assertTrue(isinstance(self.debug_app.stream_logger.handlers[0],
                                   logging.StreamHandler))
        self.assertEqual(self.debug_app.stream_logger.level, logging.DEBUG)

class FileLoggerExtensionTest(unittest.TestCase):
    def setUp(self):
        self.filepath = '%s/log' % os.path.dirname(os.path.realpath(__file__))
        self.app = WSGIApplication(
            False,
            extensions=[
                FileLoggerExtension('file', self.filepath,
                                    attr_name='file_logger')
            ]
        )
        self.debug_app = WSGIApplication(
            True,
            extensions=[
                FileLoggerExtension('debug_file', self.filepath,
                                    attr_name='file_logger')
            ]
        )

    def tearDown(self):
        os.remove(self.filepath)

    def test_app(self):
        self.assertTrue(isinstance(self.app.file_logger, logging.Logger))
        self.assertTrue(isinstance(self.app.file_logger.handlers[0],
                                   logging.FileHandler))
        self.assertEqual(self.app.file_logger.level, logging.INFO)

    def test_debug_app(self):
        self.assertTrue(isinstance(self.debug_app.file_logger, logging.Logger))
        self.assertTrue(isinstance(self.debug_app.file_logger.handlers[0],
                                   logging.FileHandler))
        self.assertEqual(self.debug_app.file_logger.level, logging.DEBUG)

if __name__ == '__main__':
    unittest.main()
