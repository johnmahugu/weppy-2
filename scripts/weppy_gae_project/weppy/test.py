from weppy.http import *

class Client(object):
    """
    HTTP client adapted to WSGIApplication.
    """

    def __init__(self, app):
        self._app = app
        self._cookies = {}

    def set_cookies(self, res):
        """
        Set cookies of an HTTPResponse to client.
        """
        cookie_header = dict(res.headerlist).get('Set-Cookie', '')
        for cookie in cookie_header.split(';'):
            if cookie:
                key, value = cookie.strip().split('=')
                self._cookies[key] = value

    def http_cookies(self):
        """
        Return an str representation of the client cookies in HTTP header format.
        """
        return ';'.join(['%s=%s' % (key, value) for key, value in self._cookies.items()])

    def get(self, path):
        """
        Return the HTTPResponse of the WSGIApplication for a GET request to path and process
        its headers.
        """
        req = HTTPRequest.get(path_info=path, headers={'HTTP_COOKIE': self.http_cookies()})
        res = self._app.handle_request(req)
        self.set_cookies(res)
        return res

    def post(self, path, params=None):
        """
        Return the HTTPResponse of the WSGIApplication for a POST request to path and process
        its headers.
        """
        req = HTTPRequest.post(path_info=path, params=params,
                               headers={'HTTP_COOKIE': self.http_cookies()})
        res = self._app.handle_request(req)
        self.set_cookies(res)
        return res

    def put(self, path, params=None):
        """
        Return the HTTPResponse of the WSGIApplication for a PUT request to path and process
        its headers.
        """
        req = HTTPRequest.put(path_info=path, params=params,
                              headers={'HTTP_COOKIE': self.http_cookies()})
        res = self._app.handle_request(req)
        self.set_cookies(res)
        return res

    def delete(self, path):
        """
        Return the HTTPResponse of the WSGIApplication for a DELETE request to path and process
        its headers.
        """
        req = HTTPRequest.delete(path_info=path, headers={'HTTP_COOKIE': self.http_cookies()})
        res = self._app.handle_request(req)
        self.set_cookies(res)
        return res

    def head(self, path):
        """
        Return the HTTPResponse of the WSGIApplication for a HEAD request to path and process
        its headers.
        """
        req = HTTPRequest.head(path_info=path, headers={'HTTP_COOKIE': self.http_cookies()})
        res = self._app.handle_request(req)
        self.set_cookies(res)
        return res
