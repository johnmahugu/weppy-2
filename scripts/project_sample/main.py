#!/usr/bin/env python

import os
import sys

from weppy.wsgi import WSGIApplication

from settings import DEBUG, CONTROLLERS, EXTENSIONS

def application(environ, start_response):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    static_root = os.path.join(dirpath, 'static')
    sys.path.insert(0, dirpath)
    app = WSGIApplication(DEBUG, CONTROLLERS, EXTENSIONS, static_root)
    return app(environ, start_response)
