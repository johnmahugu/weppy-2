import io
import sys
from webob import Request, Response
from webob.compat import url_encode
from webob.request import _encode_multipart

class HTTPRequest(object):
    """
    Wrap WebOb's Request class.
    """

    method = property(lambda self: self._req.method.upper())
    http_version = property(lambda self: self._req.http_version)
    charset = property(lambda self: self._req.charset)
    host_name = property(lambda self: self._req.host_url)
    host_port = property(lambda self: int(self._req.host_port))
    host = property(lambda self: self._req.host)
    path = property(lambda self: self._req.path)
    query_string = property(lambda self: self._req.query_string)
    url = property(lambda self: self._req.url)
    body = property(lambda self: self._req.body)
    text = property(lambda self: self._req.text)
    GET = property(lambda self: self._GET)
    POST = property(lambda self: self._POST)
    headers = property(lambda self: self._headers)
    cookies = property(lambda self: self._cookies)
    accept = property(lambda self: self._accept)
    accept_charset = property(lambda self: self._accept_charset)
    accept_encoding = property(lambda self: self._accept_encoding)
    accept_language = property(lambda self: self._accept_language)

    def __init__(self, environ):
        self._req = Request(environ)
        self._GET = dict(self._req.GET.items())
        self._POST = dict(self._req.POST.items())
        self._headers = dict(self._req.headers.items())
        self._cookies = dict(self._req.cookies.items())
        self._accept = list(self._req.accept)
        self._accept_charset = list(self._req.accept_charset)
        self._accept_encoding = list(self._req.accept_encoding)
        self._accept_language = list(self._req.accept_language)

    @classmethod
    def get(cls, http_version='HTTP/1.1', server_name='localhost', server_port=8000,
            script_name='', path_info='', query_string='', url_scheme='http', headers=None,
            multithread=True, multiprocess=False, run_once=True):
        """
        Return a GET HTTPRequest.

        http_version -- str that specifies the server protocol. 'HTTP/1.1' by default.
        server_name -- str that specifies the server name. 'localhost' by default.
        server_port -- int that specifies the server port. 8000 by default.
        script_name -- str that specifies the script name. Empty str by default.
        path_info -- str that specifies the path info. Empty str by default.
        query_string -- str that specifies the query string. Empty str by default.
        url_scheme -- str that specifies the scheme portion of the URL. 'http' by default.
        headers -- dict of HTTP headers. None by default.
        multithread -- bool that specifies wheter the request may be simultaneously invoked by
                       another thread in the same process. True by default.
        multiprocess -- bool that specifies wheter the request may be simultaneously invoked by
                        another process. False by default.
        run_once -- bool that specifies wheter the server expects (but does not guarantee) that
                    the application will only be invoked one time during the life of its
                    containing process. Normally, this will only be true for a gateway based on
                    CGI. True by default.
        """
        environ = {
            'REQUEST_METHOD': 'GET',
            'SERVER_PROTOCOL': http_version,
            'SERVER_NAME': server_name,
            'SERVER_PORT': str(server_port),
            'SCRIPT_NAME': script_name,
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url_scheme,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': multithread,
            'wsgi.multiprocess': multiprocess,
            'wsgi.run_once': run_once,
        }
        environ.update(headers or {})
        return cls(environ)

    @classmethod
    def head(cls, http_version='HTTP/1.1', server_name='localhost', server_port=8000,
             script_name='', path_info='', query_string='', url_scheme='http', headers=None,
             multithread=True, multiprocess=False, run_once=True):
        """
        Return a HEAD HTTPRequest.

        http_version -- str that specifies the server protocol. 'HTTP/1.1' by default.
        server_name -- str that specifies the server name. 'localhost' by default.
        server_port -- int that specifies the server port. 8000 by default.
        script_name -- str that specifies the script name. Empty str by default.
        path_info -- str that specifies the path info. Empty str by default.
        query_string -- str that specifies the query string. Empty str by default.
        url_scheme -- str that specifies the scheme portion of the URL. 'http' by default.
        headers -- dict of HTTP headers. None by default.
        multithread -- bool that specifies wheter the request may be simultaneously invoked by
                       another thread in the same process. True by default.
        multiprocess -- bool that specifies wheter the request may be simultaneously invoked by
                        another process. False by default.
        run_once -- bool that specifies wheter the server expects (but does not guarantee) that
                    the application will only be invoked one time during the life of its
                    containing process. Normally, this will only be true for a gateway based on
                    CGI. True by default.
        """
        environ = {
            'REQUEST_METHOD': 'HEAD',
            'SERVER_PROTOCOL': http_version,
            'SERVER_NAME': server_name,
            'SERVER_PORT': str(server_port),
            'SCRIPT_NAME': script_name,
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url_scheme,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': multithread,
            'wsgi.multiprocess': multiprocess,
            'wsgi.run_once': run_once,
        }
        environ.update(headers or {})
        return cls(environ)

    @classmethod
    def post(cls, http_version='HTTP/1.1', server_name='localhost', server_port=8000,
             script_name='', path_info='', query_string='', params=None, url_scheme='http',
             headers=None, multithread=True, multiprocess=False, run_once=True):
        """
        Return a POST HTTPRequest.

        http_version -- str that specifies the server protocol. 'HTTP/1.1' by default.
        server_name -- str that specifies the server name. 'localhost' by default.
        server_port -- int that specifies the server port. 8000 by default.
        script_name -- str that specifies the script name. Empty str by default.
        path_info -- str that specifies the path info. Empty str by default.
        query_string -- str that specifies the query string. Empty str by default.
        params -- dict that associates names and values. Files are specified by a tuple
                  (filename, content). None by default.
        url_scheme -- str that specifies the scheme portion of the URL. 'http' by default.
        headers -- dict of HTTP headers. None by default.
        multithread -- bool that specifies wheter the request may be simultaneously invoked by
                       another thread in the same process. True by default.
        multiprocess -- bool that specifies wheter the request may be simultaneously invoked by
                        another process. False by default.
        run_once -- bool that specifies wheter the server expects (but does not guarantee) that
                    the application will only be invoked one time during the life of its
                    containing process. Normally, this will only be true for a gateway based on
                    CGI. True by default.
        """
        params = params or {}
        for k, v in params.items():
            if isinstance(v, tuple):
                content_type, data = _encode_multipart(params.items(), 'multipart/form-data')
                break
        else:
            content_type = 'application/x-www-form-urlencoded'
            data = url_encode(params).encode('utf-8')
        environ = {
            'REQUEST_METHOD': 'POST',
            'SERVER_PROTOCOL': http_version,
            'SERVER_NAME': server_name,
            'SERVER_PORT': str(server_port),
            'SCRIPT_NAME': script_name,
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(len(data)),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url_scheme,
            'wsgi.input': io.BytesIO(data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': multithread,
            'wsgi.multiprocess': multiprocess,
            'wsgi.run_once': run_once,
        }
        environ.update(headers or {})
        return cls(environ)

    @classmethod
    def put(cls, http_version='HTTP/1.1', server_name='localhost', server_port=8000,
            script_name='', path_info='', query_string='', params=None, url_scheme='http',
            headers=None, multithread=True, multiprocess=False, run_once=True):
        """
        Return a PUT HTTPRequest.

        http_version -- str that specifies the server protocol. 'HTTP/1.1' by default.
        server_name -- str that specifies the server name. 'localhost' by default.
        server_port -- int that specifies the server port. 8000 by default.
        script_name -- str that specifies the script name. Empty str by default.
        path_info -- str that specifies the path info. Empty str by default.
        query_string -- str that specifies the query string. Empty str by default.
        params -- dict that associates names and values. Files are specified by a tuple
                  (filename, content). None by default.
        url_scheme -- str that specifies the scheme portion of the URL. 'http' by default.
        headers -- dict of HTTP headers. None by default.
        multithread -- bool that specifies wheter the request may be simultaneously invoked by
                       another thread in the same process. True by default.
        multiprocess -- bool that specifies wheter the request may be simultaneously invoked by
                        another process. False by default.
        run_once -- bool that specifies wheter the server expects (but does not guarantee) that
                    the application will only be invoked one time during the life of its
                    containing process. Normally, this will only be true for a gateway based on
                    CGI. True by default.
        """
        params = params or {}
        for k, v in params.items():
            if isinstance(v, tuple):
                content_type, data = _encode_multipart(params, 'multipart/form-data')
                break
        else:
            content_type = 'application/x-www-form-urlencoded'
            data = url_encode(params).encode('utf-8')
        environ = {
            'REQUEST_METHOD': 'PUT',
            'SERVER_PROTOCOL': http_version,
            'SERVER_NAME': server_name,
            'SERVER_PORT': str(server_port),
            'SCRIPT_NAME': script_name,
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(len(data)),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url_scheme,
            'wsgi.input': io.BytesIO(data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': multithread,
            'wsgi.multiprocess': multiprocess,
            'wsgi.run_once': run_once,
        }
        environ.update(headers or {})
        return cls(environ)

    @classmethod
    def delete(cls, http_version='HTTP/1.1', server_name='localhost', server_port=8000,
               script_name='', path_info='', query_string='', url_scheme='http', headers=None,
               multithread=True, multiprocess=False, run_once=True):
        """
        Return a DELETE HTTPRequest.

        http_version -- str that specifies the server protocol. 'HTTP/1.1' by default.
        server_name -- str that specifies the server name. 'localhost' by default.
        server_port -- int that specifies the server port. 8000 by default.
        script_name -- str that specifies the script name. Empty str by default.
        path_info -- str that specifies the path info. Empty str by default.
        query_string -- str that specifies the query string. Empty str by default.
        url_scheme -- str that specifies the scheme portion of the URL. 'http' by default.
        headers -- dict of HTTP headers. None by default.
        multithread -- bool that specifies wheter the request may be simultaneously invoked by
                       another thread in the same process. True by default.
        multiprocess -- bool that specifies wheter the request may be simultaneously invoked by
                        another process. False by default.
        run_once -- bool that specifies wheter the server expects (but does not guarantee) that
                    the application will only be invoked one time during the life of its
                    containing process. Normally, this will only be true for a gateway based on
                    CGI. True by default.
        """
        environ = {
            'REQUEST_METHOD': 'DELETE',
            'SERVER_PROTOCOL': http_version,
            'SERVER_NAME': server_name,
            'SERVER_PORT': str(server_port),
            'SCRIPT_NAME': script_name,
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url_scheme,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': multithread,
            'wsgi.multiprocess': multiprocess,
            'wsgi.run_once': run_once,
        }
        environ.update(headers or {})
        return cls(environ)

class HTTPResponse(object):
    """
    Wrap WebOb's Response class.
    """

    body = property(lambda self: self._res.body)
    text = property(lambda self: self._res.text)
    content_type = property(lambda self: self._res.content_type)
    status = property(lambda self: self._res.status)
    charset = property(lambda self: self._res.charset)
    headerlist = property(lambda self: self._res.headerlist)

    def __init__(self, body='', status=200, content_type='text/html',
                 charset='UTF-8', headerlist=None):
        """
        body -- str or bytes that specifies the body. Empty str by default.
        status -- int that specifies the status code. 200 by default.
        content_type -- str that specifies the content_type. 'text/html' by default.
        charset -- str that specifies the charset. 'UTF-8' by default.
        headerlist -- list of tuples that specifies the header values. None by default.
        """
        self._res = Response(body, status, headerlist, content_type=content_type,
                             charset=charset)

    def cache_expires(self, seconds):
        """
        Set the response to expire in the specified seconds.

        seconds -- int that specifies the time for the response to expire in seconds.
        """
        self._res.cache_expires(seconds)

    def set_cookie(self, key, value='', max_age=None, path='/', domain=None, secure=False,
                   httponly=False, comment=None, overwrite=False):
        """
        Set cookie.

        key -- str that specifies the cookie name.
        value -- str that specifies the cookie value. None unsets cookie. Empty str by default.
        max_age -- int that specifies the 'Max-Age' attribute in seconds. None sets a session
                   cookie. None by default.
        path -- str that specifies the 'Path' attribute. '/' by default.
        domain -- str that specifies the 'Domain' attribute. None does not set 'Domain'
                  attribute. None by default.
        secure -- bool that specifies wheter it is a secure cookie. If it is True, 'secure'
                  flag is set. If it is False, 'secure' flag is not set. False by default.
        httponly --  bool that specifies wheter it is an http only cookie. If it is True,
                     'HttpOnly' flag is set. If it is False, 'HttpOnly' flag is not set. False
                     by default.
        comment -- str that specifies the 'Comment' attribute. None does not set 'Comment'
                   attribute. None by default.
        overwrite -- bool that specifies if any existing cookie with the same key should be
                     unset before setting this cookie. False by default.
        """
        self._res.set_cookie(key, value, max_age, path, domain, secure, httponly, comment,
                             overwrite=overwrite)

    def unset_cookie(self, key):
        """
        Unset cookie with the specified key.

        key -- str that specifies the cookie name.
        """
        self._res.unset_cookie(key, False)

    def delete_cookie(self, key, path='/', domain=None):
        """
        Set cookie value to an empty str and 'Max-Age' to 0.

        key -- str that specifies the cookie name.
        path -- str that specifies the 'Path' attribute. '/' by default.
        domain -- str that specifies the 'Domain' attribute. None by default.
        """
        self._res.delete_cookie(key, path, domain)

    def __call__(self, environ, start_response):
        """
        WSGI application interface.

        environ and start_response -- objects provided by the WSGI server.
        """
        return self._res(environ, start_response)

class HTTPRedirect(HTTPResponse):
    """
    HTTP 301 or 302 response.
    """

    def __init__(self, uri, permanent=False):
        """
        uri -- str that specifies the URI that the client should be redirected to.
        permanent -- bool that specifies wheter it is a permament (status 301) or not permanent
                     (status 302) redirection. False by default.
        """
        super(HTTPRedirect, self).__init__(status=301 if permanent else 302,
                                           headerlist=[('Location', uri)])

class HTTPError(Exception, object):
    """
    Base exception for HTTP errors.
    """

    def __init__(self, status):
        """
        status -- int that specifies the status code of response.
        """
        super(HTTPError, self).__init__()
        self.status = status

    def __str__(self):
        return 'Error %s' % str(self.status)

class HTTPNotFound(HTTPError):
    """
    HTTP 404 response.
    """

    def __init__(self):
        super(HTTPNotFound, self).__init__(404)

class HTTPMethodNotAllowed(HTTPError):
    """
    HTTP 405 response.
    """

    def __init__(self):
        super(HTTPMethodNotAllowed, self).__init__(405)

class HTTPInternalServerError(HTTPError):
    """
    HTTP 500 response.
    """

    def __init__(self):
        super(HTTPInternalServerError, self).__init__(500)
