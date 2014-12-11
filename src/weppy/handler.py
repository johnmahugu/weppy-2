from weppy.http import *

class RequestHandler:
    """
    Handles requests.
    """

    def __init__(self, url_pattern, handler_name=None):
        """
        url_pattern -- str that specifies the URL pattern of the handler.
        handler_name -- str that identifies the handler. None by default.
        """
        self.url_pattern = url_pattern
        self.handler_name = handler_name

    def __call__(self, request, *args):
        """
        Processes the request with the correct method.

        request -- HTTPRequest instance.
        args -- URL parameters.
        """
        http_method = request.method.lower()
        if http_method == 'head':
            http_method = 'get'
        try:
            handler_method = getattr(self, http_method)
        except:
            raise HTTPMethodNotAllowed()
        response = handler_method(request, *args)
        if request.method.lower() == 'head':
            response = HTTPResponse('', response.status, response.content_type,
                                    response.charset, response.headerlist)
        return response

class ErrorHandler:
    """
    Handles HTTPErrors.
    """

    def error(self, http_error):
        """
        Returns a default HTTPResponse.

        http_error -- HTTPError instance.
        """
        return HTTPResponse(str(http_error), status=http_error.status)

    def __call__(self, http_error):
        """
        Processes the HTTPError with the correct method.

        http_error -- HTTPError instance.
        """
        http_error_status = str(http_error.status)
        if hasattr(self, 'error%s' % http_error_status):
            handler_method = getattr(self, 'error%s' % http_error_status)
        elif hasattr(self, 'error%sxx' % http_error_status[0]):
            handler_method = getattr(self, 'error%sxx' % http_error_status[0])
        else:
            handler_method = self.error
        return handler_method(http_error)

class url:
    """
    @url decorator that turns a class into a RequestHandler.
    """

    def __init__(self, url_pattern, handler_name=None):
        """
        url_pattern -- str that specifies the URL pattern of the handler.
        handler_name -- str that identifies the handler. None by default.
        """
        self.url_pattern = url_pattern
        self.handler_name = handler_name

    def __call__(self, cls):
        """
        cls -- class that is decorated by @url.
        """
        request_handler = type('handler', (RequestHandler,), dict(cls.__dict__))
        return request_handler(self.url_pattern, self.handler_name)
