from django.http import JsonResponse

class InternalTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.headers.get('Authorization') != 'Token miclave123':
            return JsonResponse({'error': 'No autorizado'}, status=403)
        return self.get_response(request)