from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def kb_zkt_main():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Проверка события'),
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup


def kb_zkt_event_vf():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Вернуться выше'),
        types.KeyboardButton(text='Показать список ID')
    )
    builder.row(
        types.KeyboardButton(text='Отметить'),
        types.KeyboardButton(text='Отметить изменив дату')
    )
    builder.row(
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup


def kb_zkt_sql_list():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Вернуться выше'),
        types.KeyboardButton(text='Показать список ID')
    )
    builder.row(
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup


def kb_zkt_notice():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Вернуться выше'),
        types.KeyboardButton(text='Показать список ID')
    )
    builder.row(
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup