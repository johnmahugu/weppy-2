from weppy.handler import url
from weppy.http import HTTPResponse

@url('/wall/')
class WallHandler:
    def get(self, request):
        return HTTPResponse('["Hello, World!", "Ola, Mundo!"]')
