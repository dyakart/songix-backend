from django.core.management.base import BaseCommand
from ...source.app import start  # Импортируем функцию для запуска бота


class Command(BaseCommand):
    help = 'Запускает Telegram-бота'

    def handle(self, *args, **kwargs):
        # запускаем нашего бота отдельно без django (для отладки)
        start()
