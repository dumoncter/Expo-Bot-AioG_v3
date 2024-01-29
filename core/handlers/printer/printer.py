import asyncio
from datetime import datetime
from aiogram import types, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.keyboards.zkt_kb import kb_zkt_event_vf, kb_zkt_main
from core.keyboards.main_kb import get_reply_main
from .zkt_sql_inject import sql_inject
import json

router = Router()


# FSM States
class ClientState(StatesGroup):
    INJECT_MAIN = State()


@router.message(F.text.lower() == "принтер")
async def answer_no(message: Message):
    await message.answer(
        f"<b>Утилита для калибровки устройств Zebra:</b>\n"
        f"☑ Выберете действие:",
        reply_markup=kb_zkt_main()
    )






