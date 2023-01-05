from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def show_field(field:list|str):
    """
    :param field: Передайте на значение этого параметра двумерный массив с полем или строку "start", если хотите оставить поле пустым
    :return: InlineKeyboardMarkup c вашим полем.
    """
    builder = InlineKeyboardBuilder()
    
    if field == 'start':
        field = [[' ' for j in range(8)] for i in range(8)]

    builder.row(
        *[InlineKeyboardButton(text=j[1], callback_data=f'{i[0]}:{j[0]}') for i in enumerate(field) for j in enumerate(i[1])],
        width=8
    )

    return builder.as_markup()

def is_ready():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Да', callback_data='y'),
        InlineKeyboardButton(text='Нет', callback_data='n')
    )

    return builder.as_markup()