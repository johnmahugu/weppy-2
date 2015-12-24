import re
from weppy.http import *

class Handler(object):
    """
    Handle requests.
    """

    def __init__(self, url_pattern):
        self._url_regex = re.compile(r'^%s$' % re.escape(url_pattern).replace('\_', '([^/]+)'))

    def __call__(self, req, *args):
        """
        Call the appropriate handler method and return an HTTPResponse, or raise an
        HTTPMethodNotAllowed exception if it does not exist.
        """
        http_method = req.method.lower()
        if http_method == 'head':
            http_method = 'get'
        try:
            handler_method = getattr(self, http_method)
        except:
            raise HTTPMethodNotAllowed()
        res = handler_method(req, *args)
        if isinstance(res, str):
            res = HTTPResponse(res)
        if req.method.lower() == 'head':
            res = HTTPResponse('', res.status, res.content_type, res.charset, res.headerlist)
        return res

class url(object):
    """
    Decorator to turn a class into a Handler instance.
    """

    def __init__(self, url_pattern):
        self._url_pattern = url_pattern

    def __call__(self, cls):
        """
        Return an instance of a new type inherited from Handler and with the decorated class
        methods.
        """
        handler = type('handler', (Handler,), dict(cls.__dict__))
        return handler(self._url_pattern)
