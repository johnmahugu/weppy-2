from weppy.http import *

class login_required:
    """
    Decorator for method that checks if the user is logged in. If it is not,
    redirects to the login page.
    """

    def __init__(self, login_url):
        """
        login_url -- URL of the login page.
        """
        self.login_url = login_url

    def __call__(self, method):
        """
        method -- handler method.
        """
        def wrapped_method(handler, request, *args, **kwargs):
            if request.session.user is None:
                return HTTPRedirect(self.login_url)
            return method(handler, request, *args, **kwargs)
        return wrapped_method
