from aiogram.types.web_app_info import WebAppInfo
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# MAIN (specify ip)
def zywall_main():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Запустить утилиту',
                             web_app=WebAppInfo(url='https://expo-torg.ddns.me:35800/telegram_web/')),
        types.KeyboardButton(text='В главное меню')
    )
    reply_markup = builder.as_markup(resize_keyboard=True, input_field_placeholder='Выберете действие:')
    return reply_markup
