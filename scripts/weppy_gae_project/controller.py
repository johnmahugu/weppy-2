from weppy.handler import url

@url('/')
class HelloWorldHandler:
    def get(self, request):
        return 'Hello, World!'
