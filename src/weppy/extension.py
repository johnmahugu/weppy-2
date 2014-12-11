class Extension:
    """
    Plugin system for manipulating WSGIApplication, HTTPRequest and HTTPResponse
    instances.

    The '__call__' method is called before any request is accepted by the
    server.

    The 'process_request' method is called before each request is processed by a
    handler.

    The 'process_response' method is called after each request is processed by a
    handler.
    """

    def __call__(self, app):
        """
        app -- WSGIApplication instance.
        """
        pass

    def process_request(self, request):
        """
        request -- HTTPRequest instance.
        """
        pass

    def process_response(self, request, response):
        """
        request -- HTTPRequest instance.
        response -- HTTPResponse instance.
        """
        pass
