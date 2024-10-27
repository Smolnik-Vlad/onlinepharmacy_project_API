import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)

class LogHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Логируем заголовки запроса
        print("Request Headers: %s", request.headers)

        # Обработка запроса
        response = self.get_response(request)

        # Логируем заголовки ответа (если требуется)
        print("Response Headers: %s", response.headers)

        return response
