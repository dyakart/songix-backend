import os
from django.apps import AppConfig
import threading
from .source.app import start  # Импорт функции `start` для запуска бота
# импортируем наши данные из env файла
from dotenv import load_dotenv

# загружаем данные
load_dotenv()


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        # Проверяем, что это основной процесс, чтобы избежать дублирования запуска бота в режиме автообновления
        if os.getenv('RUN_MAIN') == 'true':
            # Создаем и запускаем отдельный поток для бота
            thread = threading.Thread(target=start)
            thread.daemon = True  # Поток завершится вместе с основным процессом
            thread.start()
