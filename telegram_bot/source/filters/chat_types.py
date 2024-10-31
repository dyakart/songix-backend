# фильтры, которые будут фильтровать события в зависимости от того, где написаны сообщения (в личке, в группе, супергруппе)

from aiogram.filters import Filter
from aiogram import Bot, types


# создаём свой фильтр для чатов
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]):
        # получаем список типов чатов (личка, группа, супергруппа), где будет работать роутер
        self.chat__types = chat_types

    # переопределяем вызов объекта
    async def __call__(self, message: types.Message):
        # если сообщение пользователя соответствует типу, на котором работает роутер, то отправляем ответ
        return message.chat.type in self.chat__types


# создаём фильтр для проверки является ли пользователь администратором
class IsAdmin(Filter):
    def __init__(self):
        pass

    # если id пользователя есть в списке администраторов, возвращаем True
    async def __call__(self, message: types.Message, bot: Bot):
        return message.from_user.id in bot.my_admins_list
