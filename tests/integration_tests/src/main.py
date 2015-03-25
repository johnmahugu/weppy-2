#!/usr/bin/env python

from weppy.wsgi import *
from settings import DEBUG, CONTROLLERS

application = WSGIApplication(DEBUG, CONTROLLERS)
