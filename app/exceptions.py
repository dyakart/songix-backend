from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Получаем стандартный ответ от DRF
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        # Собираем все сообщения об ошибках в список
        errors = []
        for message_list in response.data.values():
            if isinstance(message_list, list):
                errors.extend(message_list)
            else:
                errors.append(message_list)

        # Возвращаем единый ответ с ключом "error" и списком сообщений
        response.data = {
            "error": errors
        }

    return response
