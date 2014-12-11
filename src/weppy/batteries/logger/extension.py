import logging
import sys

from weppy.extension import Extension

class StreamLoggerExtension(Extension):
    """
    Sets a logger to the standard output in the request object.
    """

    def __init__(self, name, format=None, attr_name='logger'):
        """
        name -- str that specifies the name of the log.
        format -- str that specifies the format of the log. None by default.
        attr_name -- str that specifies the name of the attribute of the app
                     object in which the logger is set. 'logger' by default.
        """
        self.attr_name = attr_name
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler(sys.stdout)
        if format is not None:
            handler.setFormatter(logging.Formatter(format))
        self.logger.addHandler(handler)

    def __call__(self, app):
        """
        Sets the logger in the app object.

        app -- WSGIApplication instance.
        """
        self.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
        setattr(app, self.attr_name, self.logger)

class FileLoggerExtension(Extension):
    """
    Sets a logger to the specified file in the request object.
    """

    def __init__(self, name, filepath, format=None, attr_name='logger'):
        """
        name -- str that specifies the name of the log.
        filepath -- str that specifies the path to the log file.
        format -- str that specifies the format of the log. None by default.
        attr_name -- str that specifies the name of the attribute of the app
                     object in which the logger is set. 'logger' by
                     default.
        """
        self.attr_name = attr_name
        self.logger = logging.getLogger(name)
        handler = logging.FileHandler(filepath)
        if format is not None:
            handler.setFormatter(logging.Formatter(format))
        self.logger.addHandler(handler)

    def __call__(self, app):
        """
        Sets the logger in the app object.

        app -- WSGIApplication instance.
        """
        self.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
        setattr(app, self.attr_name, self.logger)
