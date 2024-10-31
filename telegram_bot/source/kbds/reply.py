# ответы бота в виде клавиатуры

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# получаем данные для клавиатуры
def get_keyboard(
        # передаем текст кнопок
        *btns: str,
        # подсказку в поле ввода
        placeholder: str = None,
        # индекс кнопки номера телефона
        request_contact: int = None,
        # индекс кнопки локации
        request_location: int = None,
        # расположение кнопок на клавиатуре (например, (2,1) - две в первой строке, одна во второй и тд)
        sizes: tuple = (2,),
):
    """
    Создает клавиатуру с кнопками и настраиваемыми параметрами.

    Параметры:
    - btns (str): Текст кнопок для клавиатуры.
    - placeholder (str): Подсказка для поля ввода (отображается при открытии клавиатуры).
    - request_contact (int): Индекс кнопки, запрашивающей номер телефона.
    - request_location (int): Индекс кнопки, запрашивающей локацию.
    - sizes (tuple): Расположение кнопок на клавиатуре (например, (2,1) — две кнопки в первой строке, одна во второй).

    Пример:
    get_keyboard(
        'Меню', 'О магазине', 'Варианты оплаты', 'Варианты доставки', 'Отправить номер телефона',
        placeholder='Что Вас интересует?',
        request_contact=4,
        sizes=(2, 2, 1)
    )
    keyboard = ReplyKeyboardBuilder()
    """
    keyboard = ReplyKeyboardBuilder()

    # Проверка значений request_contact и request_location на корректность
    if request_contact is not None and request_contact >= len(btns):
        raise ValueError("Значение request_contact выходит за пределы списка кнопок.")
    if request_location is not None and request_location >= len(btns):
        raise ValueError("Значение request_location выходит за пределы списка кнопок.")

    # Проходимся по кнопкам и добавляем их с нужными параметрами
    for index, text in enumerate(btns):
        if index == request_contact:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif index == request_location:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    # Проверка на корректность sizes
    total_buttons = len(btns)
    if sum(sizes) != total_buttons:
        print(
            f"Предупреждение: сумма элементов sizes ({sum(sizes)}) не совпадает с количеством кнопок ({total_buttons}).")

    # Устанавливаем размеры и подсказку для клавиатуры
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )
