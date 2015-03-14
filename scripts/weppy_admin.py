#!/usr/bin/env python

import os
import sys
from subprocess import call
from argparse import ArgumentParser

def runserver(args):
    """
    Start WSGI server on the specified port.
    """
    sys.path.insert(0, args.path)
    from main import application
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', args.port, application)
    server.serve_forever()

def startproject(args):
    """
    Copy Weppy sample project structure to the current directory.
    """
    source = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weppy_project')
    destination = os.path.join(os.getcwd(), args.name)
    call('cp -R %s %s' % (source, destination), shell=True)

def main():
    """
    Parse arguments and run the specified action or show help text.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    runserver_parser = subparsers.add_parser('runserver')
    runserver_parser.add_argument('-p', '--port', type=int, dest='port', default=8000,
                                  help='run server on the specified port')
    runserver_parser.add_argument('-P', '--path', type=str, dest='path', default='.',
                                  help='path of Weppy project directory')
    runserver_parser.set_defaults(func=runserver)
    startproject_parser = subparsers.add_parser('startproject')
    startproject_parser.add_argument('name', default='src',
                                     help='name of Weppy project directory')
    startproject_parser.set_defaults(func=startproject)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
