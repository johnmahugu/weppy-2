#!/usr/bin/env python

import os
import sys
from weppy.wsgi import *
from settings import DEBUG, CONTROLLERS

def application(environ, start_response):
    return WSGIApplication(DEBUG, CONTROLLERS)(environ, start_response)
