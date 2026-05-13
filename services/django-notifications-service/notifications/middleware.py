import os
from django.http import JsonResponse

class InternalTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token = os.environ.get('TOKEN_SECRETO')
        if not self.token:
            raise ValueError("La variable de entorno TOKEN_SECRETO no está definida.")

    def __call__(self, request):
        if request.headers.get('Authorization') != f'Token {self.token}':
            return JsonResponse({'error': 'No autorizado'}, status=403)
        return self.get_response(request)