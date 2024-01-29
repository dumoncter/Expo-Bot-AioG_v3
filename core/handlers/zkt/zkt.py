import asyncio
import re
from datetime import datetime, time
from aiogram import types, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.keyboards.zkt_kb import kb_zkt_event_vf, kb_zkt_main, kb_zkt_notice
from core.keyboards.main_kb import get_reply_main
from .zkt_sql_inject import sql_inject
import json

router = Router()


# FSM States
class ClientState(StatesGroup):
    INSERT_TIME = State()
    INJECT_MAIN = State()
    INSERT_HOURS = State()


text_zkt = '''
✅ Укажите, через пробел: \n
<b>1 - ID сканера</b> и 2 - <b>ID учетной записи</b> на котором проводится проверка. \n
Пример: 
<b>54 988</b>'''


@router.message(F.text.lower() == "zkt")
async def answer_no(message: Message):
    await message.answer(
        f"<b>Утилита для работы с устройствами СКУД ZKT:</b>\n"
        f"☑ Выберете действие:",
        reply_markup=kb_zkt_main()
    )


@router.message(F.text.lower() == "проверка события")
async def event_verification(message: types.Message) -> None:
    await message.reply("<b>Для работы необходимо узнать требуемый ID сканера.</b>\n"
                        "Найдите требуемый из списка.\n"
                        "<u>Если ID уже известен, переходите <b>далее - 'Отметить'</b></u>",
                        reply_markup=kb_zkt_event_vf())


@router.message(F.text.lower() == "показать список id")
async def search_zkt_id(message: types.Message) -> None:
    await message.answer(open_file())
    await message.answer("❗ <u><b>Повторное использование через минуту</b></u>", reply_markup=kb_zkt_event_vf())


def open_file():
    with open("zkt_ip.json", 'r', encoding='utf-8') as f:
        contents = json.load(f)
        new_line = '\n'
        id_list = []
        for i in range(len(contents)):
            id_list.append('ID: ' + '<b>' + str(contents[i]['ID']) + '</b>' + ' = ' + contents[i]['Name'])
        return new_line.join(list(map(str, id_list)))


@router.message(F.text.lower() == "отметить")
async def notice(message: types.Message, state: FSMContext):
    await message.reply("✅ Укажите, через пробел: \n"
                        "<b>1 - ID сканера</b> и 2 - <b>ID учетной записи</b> на котором проводится проверка. \n"
                        "Пример: "
                        "<b>54 988</b>", reply_markup=kb_zkt_notice())
    await state.set_state(ClientState.INJECT_MAIN)


@router.message(F.text.lower() == "отметить изменив дату")
async def notice(message: types.Message, state: FSMContext):
    await message.reply("✅ Укажите, желаемое время: \n"
                        "Пример: <b>17:23</b>", reply_markup=kb_zkt_notice())
    await state.set_state(ClientState.INSERT_TIME)


@router.message(ClientState.INSERT_TIME)
async def func_inject(message: types.Message, state: FSMContext):
    entered_time = message.text
    pattern = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
    current_time = datetime.now().time()
    hours, minutes = map(int, entered_time.split(':'))
    compare_time = time(hours, minutes)
    if not re.match(pattern, entered_time):
        await message.reply('Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.')
        return
    elif compare_time > current_time:
        await message.reply(f'<b>⛔ Время не может быть больше нынешнего.</b>\n'
                            f'Текущее время <b>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</b>')
        return
    else:
        await state.update_data(hours=hours)
        await state.update_data(minutes=minutes)
        await message.reply("✅ Укажите, через пробел: \n"
                            "<b>1 - ID сканера</b> и 2 - <b>ID учетной записи</b> на котором проводится проверка. \n"
                            "Пример: "
                            "<b>54 988</b>", reply_markup=kb_zkt_notice())
        await state.set_state(ClientState.INJECT_MAIN)


@router.message(ClientState.INJECT_MAIN)
async def func_inject(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    hours, minutes = context_data.get('hours'), context_data.get('minutes')
    user_msg = message.text
    formatted = user_msg.split()
    if user_msg.isalpha():
        await message.reply('⛔ Сообщение не может содержать буквы .\n')
    elif len(formatted) >= 3:
        await message.reply('⛔ Сообщение не может содержать более двух аргументов .\n'
                            'Пример: ID учетной записи: <b>1450</b>, ID сканера: <b>48</b>\n'
                            '<b><u>1450 48</u></b>')
    elif len(message.text) > 8:
        await message.reply('⛔ Не корректный ввод.\n'
                            'ID учетной записи может содержать <b>более 9999</b> номеров\n'
                            'ID сканера не более <b>999</b>\n'
                            'Пример: ID учетной записи: <b>1450</b>, ID сканера: <b>48</b>\n'
                            '<b><u>1450 48</u></b>')
    elif not user_msg:
        await message.reply('Сообщение не может быть пустым')
    else:
        inject = asyncio.create_task(sql_inject(formatted[0], formatted[1], hours, minutes))
        await inject
        result = inject.result()
        await message.answer(result, reply_markup=get_reply_main())
        await state.clear()
