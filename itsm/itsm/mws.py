'''
Middlewares
'''
def simple_middleware(get_response):
    def middleware(request):
        print('Before the view ...')
        response = get_response(request)
        print('After the view ...')
        return response
    return middleware