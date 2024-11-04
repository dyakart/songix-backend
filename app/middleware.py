from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware


class CustomCsrfMiddleware(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Возвращаем JSON-ответ вместо HTML
        return JsonResponse({'error': 'CSRF token missing or incorrect'}, status=403)
