import ipaddress
from aiogram import types, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from pythonping import ping
from core.keyboards.nettols_kb import net_tools_main, ping_kb

router = Router()


class ClientState(StatesGroup):
    PING = State()


@router.message(F.text.lower() == "проверка сети")
async def main_net_tools(message: types.Message):
    await message.reply("Выберете функцию:", reply_markup=net_tools_main())


@router.message(F.text.lower() == "ping")
async def icmp_ping(message: types.Message, state: FSMContext):
    await message.reply("Утилита для работы с <b>ICMP</b>. Укажите IP без приставки <b>192.168</b>\n"
                        "Пример: <b>20.1</b>\n"
                        "",
                        reply_markup=ping_kb())
    await state.set_state(ClientState.PING)


@router.message(ClientState.PING)
async def run_ping(message: types.Message, state: FSMContext):
    user_msg = message.text
    reduced = user_msg.split('.')
    line = '-' * 55
    first_ip = '192.168'
    if len(reduced) == 2 and len(reduced[0]) <= 3 and len(reduced[1]) <= 3:
        if reduced[0].isdigit() and reduced[1].isdigit():
            await message.reply("<b>🔥 Запрос обрабатывается</b>")
            await message.reply(f'<b>Ваш адрес: {first_ip + "." + reduced[0] + "." + reduced[1]}\n'
                                f'{line}\n'
                                f'{ping(first_ip + "." + reduced[0] + "." + reduced[1], count=5)}</b>',
                                reply_markup=net_tools_main())
            await message.answer(f'⚠️ Если требуется проверить другой адрес, <b>то в этом окне укажите <u>новый ip адрес.</u>\n</b>'
                                 f'Для завершения работы нажмите - <b><u>В главное меню</u></b>')
            # await state.finish()
        else:
            await message.reply("❌ <b>Адрес указан не корректно, повторите снова</b>")

    elif len(reduced) == 4:
        try:
            ip = ipaddress.ip_address(user_msg)
            await message.reply(f'<b>Ваш адрес: {first_ip + "." + reduced[0] + "." + reduced[1]}\n'
                                f'{line}\n'
                                f'{ping(user_msg, count=5)}</b>',
                                reply_markup=ping_kb())
            await message.answer(f'''
⚠️ Если требуется проверить другой адрес, <b>то в этом окне укажите новый ip адрес.</b>
Для завершения работы нажмите <b>В главное меню</b>''')
            # await state.finish()
        except ValueError:
            await message.reply("❌ <b>Адрес указан не корректно, повторите снова</b>")
    else:
        await message.reply("❌ <b>Адрес указан не корректно, повторите снова</b>")

