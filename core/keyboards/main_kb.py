from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_main():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Поиск по MAC'),
        types.KeyboardButton(text='ZKT')
    )
    builder.row(
        types.KeyboardButton(text='Проверка сети')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup


# inline keyboard
def get_inline_main():
    buttons = [
        [types.InlineKeyboardButton(text='Посмотреть список обновлений', callback_data='updates')],
        [types.InlineKeyboardButton(text='Список будующих изменений', callback_data='updates')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
