# точка входа

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode  # импортируем класс для форматирования текста
from aiogram.client.default import DefaultBotProperties  # импортируем класс для настроек бота
import aiohttp  # Асинхронная библиотека для HTTP-запросов
# библиотеки для автоматического нахождения нашего файла dotenv и его загрузки
from dotenv import find_dotenv, load_dotenv
from django.conf import settings  # импортируем настройки django

load_dotenv(find_dotenv())

# наши импорты
from telegram_bot.source.handlers.user_private import user_private_router  # импортируем наш роутер для обработки событий в личке
from telegram_bot.source.common.bot_cmds_list import private  # импортируем наши команды для бота (private - для личных сообщений)
# импортируем глобальные переменные
from telegram_bot.source.singleton import global_vars

# указываем какие именно изменения отслеживаем у сервера telegram
ALLOWED_UPDATES = ['message, edited_message']

# инициализируем класс бота, передаем токен
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# создаем класс диспетчера, который отвечает за фильтрацию разных сообщений (сообщения от сервера telegram)
dp = Dispatcher()

# подключаем наши роутеры (работают в том же порядке)
dp.include_routers(user_private_router)


async def main():
    """Метод запуска бота"""

    # Глобальная сессия aiohttp для всех API-запросов
    session = aiohttp.ClientSession()
    global_vars.session = session  # Устанавливаем глобальную сессию
    try:
        # отвечаем только, когда бот онлайн
        await bot.delete_webhook(drop_pending_updates=True)
        # удалить все наши команды для лички
        # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
        # отправляем все наши команды, которые будут у бота (только в личке)
        await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
        # слушаем сервер telegram и постоянно спрашиваем его про наличие каких-то изменений
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    finally:
        # Закрываем сессию при завершении работы
        await session.close()


def start():
    # запускаем нашу функцию main
    asyncio.run(main())
