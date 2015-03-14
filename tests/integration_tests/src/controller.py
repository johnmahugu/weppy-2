from weppy.handler import *
from weppy.http import *

@url('/golden/corn/')
class GoldenCornHandler:
    def get(self, req):
        return HTTPResponse('Lets get the golden corn!')

    def post(self, req):
        return HTTPResponse('Lets post the golden corn!')

@url('/metal/_/food/_/')
class MetalFoodHandler:
    def get(self, req, metal, food):
        return HTTPResponse('Lets get the %s %s!' % (metal, food))

    def post(self, req, metal, food):
        return HTTPResponse('Lets post the %s %s!' % (metal, food))
