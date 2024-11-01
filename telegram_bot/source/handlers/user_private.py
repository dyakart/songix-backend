# обработчики событий, которые относятся к общению бота с пользователем в личке

import os
from aiogram import F, types, Router
# импортируем инлайн клавиатуры и web app
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
# для обработки HTML
from aiogram.enums import ParseMode
# импортируем систему фильтрации сообщений и для работы с командами
from aiogram.filters import CommandStart, Command, or_f, StateFilter
# импортируем библиотеки для работы со стояниями
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
# импортируем классы для форматирования текста
from aiogram.utils.formatting import as_list, as_marked_section, Bold
import aiohttp  # Асинхронная библиотека для HTTP-запросов

# наши импорты
# импортируем фильтр для определения личка, группа, супергруппа
from ..filters.chat_types import ChatTypeFilter
# импортируем ответные клавиатуры
from ..kbds.reply import get_keyboard
# импортируем методы для лички
# from actions.private import
# импортируем глобальные переменные
from ..singleton import global_vars

# создаем отдельный роутер для сообщений лички
user_private_router = Router()
# подключаем фильтр для определения, где будет работать роутер (в личке, в группе, супергруппе)
user_private_router.message.filter(ChatTypeFilter(['private']))

# Словарь для клавиатур
KEYBOARDS = {
    "launch": InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Запустить Songix",
            web_app=WebAppInfo(url=global_vars.domain)
        )]
    ]),
    "cancel": get_keyboard("Отменить", placeholder="Выберите действие", sizes=(1,))
}


# Вспомогательная функция для отправки ответов с клавиатурой
async def send_message_with_keyboard(message: types.Message, text: str, keyboard_type: str) -> None:
    await message.answer(text, reply_markup=KEYBOARDS[keyboard_type])


# Обработчик для команды /start
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await send_message_with_keyboard(
        message,
        "Привет, я Songix бот!\nНажмите на кнопку ниже, чтобы запустить Songix",
        "launch"
    )


# Обработчик для команды /launch
@user_private_router.message(Command("launch"))
async def launch_web_app_cmd(message: types.Message):
    await send_message_with_keyboard(
        message,
        "Нажмите на кнопку ниже, чтобы запустить Songix:",
        "launch"
    )


# Код ниже для машины состояний (FSM)


# обработчик для отмены всех состояний
# добавляем StateFilter('*'), где '*' - любое состояние пользователя
@user_private_router.message(StateFilter('*'), Command("отменить"))
@user_private_router.message(StateFilter('*'), F.text.lower() == "отменить")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    # Получаем текущее состояние
    current_state = await state.get_state()

    # Если у пользователя нет состояния, то выходим из обработчика
    if current_state:
        # Очищаем все состояния пользователя
        await state.clear()

    # Отправляем сообщение об отмене и возвращаем начальную клавиатуру
    await send_message_with_keyboard(message, "Действия отменены", "launch")
