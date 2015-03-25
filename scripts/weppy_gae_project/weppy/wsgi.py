import inspect
import traceback
from weppy.handler import *
from weppy.http import *

class WSGIApplication(object):
    """
    WSGI application interface.
    """

    def __init__(self, debug, controllers=None):
        """
        Inspect controller modules to find Handler instances.
        """
        self._debug = debug
        self._routes = {}
        for controller in controllers or []:
            for name, obj in inspect.getmembers(controller):
                if isinstance(obj, Handler):
                    self.add_handler(obj)

    def add_handler(self, handler):
        """
        Add a Handler instance to this application.
        """
        self._routes[handler._url_regex] = handler

    def handle_request(self, req):
        """
        Return an HTTPResponse processed by the appropriate Handler instance or by catching an
        exception, or redirect the request by appending a slash to its path.
        """
        try:
            for (url_regex, handler) in self._routes.items():
                match = url_regex.match(req.path)
                if match is not None:
                    return handler(req, *match.groups())
            for (url_regex, handler) in self._routes.items():
                match = url_regex.match(req.path + '/')
                if match is not None:
                    return HTTPRedirect(req.path + '/')
            raise HTTPNotFound()
        except Exception as error:
            if not isinstance(error, HTTPError):
                if self._debug:
                    traceback.print_exc()
                error = HTTPInternalServerError()
            return HTTPResponse(str(error), status=error.status)

    def __call__(self, environ, start_response):
        """
        WSGI interface.
        """
        return self.handle_request(HTTPRequest(environ))(environ, start_response)
