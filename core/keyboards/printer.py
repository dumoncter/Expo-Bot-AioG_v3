from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def printer_main():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup



