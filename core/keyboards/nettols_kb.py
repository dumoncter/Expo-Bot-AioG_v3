from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


# netttols main kb
def net_tools_main():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='PING'),
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup


# ping kb
def ping_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Повторить'),
        types.KeyboardButton(text='В главное меню'),
        types.KeyboardButton(text='Изменить размер пакета'),
        types.KeyboardButton(text='Установить количество пакетов'),
        types.KeyboardButton(text='Проверка MTU (Опр. макс. пакета)'),
        types.KeyboardButton(text='Расширенная версия'),
    )
    builder.adjust(2)
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup

