import inspect
import mimetypes
import os
import re
import traceback

from weppy.handler import ErrorHandler, RequestHandler
from weppy.http import *
from weppy.exception import MultipleErrorHandler

class WSGIApplication:
    """
    WSGI application interface.
    """

    def __init__(self, debug, controllers=None, extensions=None,
                 static_root=None):
        """
        debug -- bool that specifies wheter it is a development environment.
        controllers -- list of controller modules containing the request
                       handlers and error handler of the application. None by
                       default.
        extensions -- list of extensions. None by default.
        static_root -- str that specifies the path of the static root directory
                       of the application. None by default.
        """
        self._debug = debug
        self._extensions = extensions or []
        self._static_root = static_root
        self._routes = {}
        self._reverse_routes = {}
        self._error_handler = None
        for controller in controllers or []:
            for name, obj in inspect.getmembers(controller):
                if isinstance(obj, RequestHandler):
                    self.add_request_handler(obj)
                if isinstance(obj, ErrorHandler):
                    if self._error_handler is not None:
                        raise MultipleErrorHandler('Multiple ErrorHandlers '
                                                   'defined in controllers.')
                    self.set_error_handler(obj)
        if self._error_handler is None:
            self.set_error_handler(ErrorHandler())
        for extension in self._extensions:
            extension(self)

    # Properties to access app attributes.
    debug = property(lambda self: self._debug)

    def add_request_handler(self, request_handler):
        """
        Adds a RequestHandler instance to the application.

        request_handler -- RequestHandler instance.
        """
        request_handler.app = self
        url_pattern_regex = re.compile(
            r'^%s$' %
            re.escape(request_handler.url_pattern).replace('_', '([^/]+)')
        )
        self._routes[url_pattern_regex] = request_handler
        if request_handler.handler_name is not None:
            url_pattern_escaped = request_handler.url_pattern.replace('_', '%s')
            self._reverse_routes[request_handler.handler_name] = \
                    url_pattern_escaped

    def set_error_handler(self, error_handler):
        """
        Sets the application ErrorHandler instance.

        error_handler -- ErrorHandler instance.
        """
        error_handler.app = self
        self._error_handler = error_handler

    def reverse(self, handler_name, *args):
        """
        Returns a str of the URL of the handler identified by handler_name and
        the arguments in args or raises an exception if the specified handler
        does not exist or the arguments are invalid.

        handler_name -- str that identifies the handler to be used.
        args -- tuple of Python objects to fill the URL parameters.
        """
        if handler_name in self._reverse_routes:
            return self._reverse_routes[handler_name] % args
        raise ValueError(
            '%s is not a handler specified in the application.' % handler_name
        )

    def _responsible_match_and_handler(self, path):
        """
        Returns a tuple of the URL regular expression match instance and the
        associated handler or None if the path does not match with any URL
        regular expression pattern of the routes.

        path -- str that specifies the request path.
        """
        for (regex, handler) in self._routes.items():
            match = regex.match(path)
            if match is not None:
                return (match, handler)
        return None

    def _controller(self, request):
        """
        Calls the appropriate handler for the request and returns an
        HTTPResponse instance or raises an HTTPNotFound exception.

        request -- HTTPRequest instance.
        """
        path = request.path
        match_handler = self._responsible_match_and_handler(path)
        if match_handler is not None:
            match, handler = match_handler
            for extension in self._extensions:
                extension.process_request(request)
            response = handler(request, *match.groups())
            for extension in self._extensions:
                extension.process_response(request, response)
            return response
        if path.endswith('/') is False and \
           self._responsible_match_and_handler(path + '/') is not None:
            return HTTPRedirect(path + '/')
        if path.startswith('/static/') and self._debug and self._static_root:
            relative_path = path[len('/static/'):]
            filepath = os.path.join(self._static_root, relative_path)
            content_type, charset = mimetypes.guess_type(path)
            try:
                file = open(filepath, 'rb')
            except:
                raise HTTPNotFound()
            content = file.read()
            file.close()
            return HTTPResponse(content, content_type=content_type,
                                charset=charset)
        raise HTTPNotFound()

    def _handle_request(self, request):
        """
        Returns an HTTPResponse instance.

        request -- HTTPRequest instance.
        """
        try:
            response = self._controller(request)
        except Exception as error:
            if not isinstance(error, HTTPError):
                if self._debug:
                    traceback.print_exc()
                error = HTTPInternalServerError()
            response = self._error_handler(error)
        return response

    def __call__(self, environ, start_response):
        """
        WSGI application interface.

        environ and start_response -- objects provided by the WSGI server.
        """
        request = HTTPRequest(environ)
        return self._handle_request(request)(environ, start_response)
