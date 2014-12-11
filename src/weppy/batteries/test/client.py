from weppy.http import *

class Client:
    """
    Simulates requests to the specified WSGIApplication.
    """

    def __init__(self, app):
        """
        app -- WSGIApplication instance.
        """
        self._app = app
        self._cookies = {}

    def _process_response(self, response):
        """
        Adds the cookies set in response to the client.

        response -- HTTPResponse instance.
        """
        cookie_header = dict(response.headerlist).get('Set-Cookie', '')
        for cookie in cookie_header.split(';'):
            if cookie:
                k, v = cookie.strip().split('=')
                self._cookies[k] = v

    def _headers(self):
        """
        Returns a dict that specifies the client HTTP headers.
        """
        return {
            'HTTP_COOKIE': ';'.join(
                ['%s=%s' % (k, v) for k, v in self._cookies.items()]
            )
        }

    def get(self, path):
        """
        Simulates a GET request and returns an HTTPResponse.

        path -- str that specifies the path that is tested.
        """
        req = HTTPRequest.get(path_info=path, headers=self._headers())
        res = self._app._handle_request(req)
        self._process_response(res)
        return res

    def post(self, path, params=None):
        """
        Simulates a POST request and returns an HTTPResponse.

        path -- str that specifies the path that is tested.
        params -- dict that associates names and values. Files are specified by
                  a tuple (filename, content). None by default.
        """
        req = HTTPRequest.post(path_info=path, params=params,
                               headers=self._headers())
        res = self._app._handle_request(req)
        self._process_response(res)
        return res

    def put(self, path, params=None):
        """
        Simulates a PUT request and returns an HTTPResponse.

        path -- str that specifies the path that is tested.
        params -- dict that associates names and values. Files are specified by
                  a tuple (filename, content). None by default.
        """
        req = HTTPRequest.put(path_info=path, params=params,
                              headers=self._headers())
        res = self._app._handle_request(req)
        self._process_response(res)
        return res

    def delete(self, path):
        """
        Simulates a DELETE request and returns an HTTPResponse.

        path -- str that specifies the path that is tested.
        """
        req = HTTPRequest.delete(path_info=path, headers=self._headers())
        res = self._app._handle_request(req)
        self._process_response(res)
        return res

    def head(self, path):
        """
        Simulates a HEAD request and returns an HTTPResponse.

        path -- str that specifies the path that is tested.
        """
        req = HTTPRequest.head(path_info=path, headers=self._headers())
        res = self._app._handle_request(req)
        self._process_response(res)
        return res
