import smtplib
import unittest
from io import StringIO
from unittest.mock import patch

from weppy.batteries.mail import MailExtension
from weppy.wsgi import WSGIApplication

class MailExtensionTest(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_send(self, stdout_mock):
        app = WSGIApplication(True)
        mail_ext = MailExtension(True, '0.0.0.0', 20)
        mail_ext(app)
        app.mail_server.send('abc@domain.com', 'def@domain.com', 'Hello, world')
        self.assertEqual(
            stdout_mock.getvalue(),
            'From: abc@domain.com\nTo: [\'def@domain.com\']\nHello, world\n'
        )

    @patch.object(smtplib, 'SMTP')
    def test_valid_server(self, smtp_mock):
        mail_ext = MailExtension(False, 'localhost', 20)
        smtp_mock.assert_called_with('localhost', 20)

    def test_invalid_server(self):
        self.assertRaises(Exception, MailExtension, False, '0.0.0.0', 20)

if __name__ == '__main__':
    unittest.main()
