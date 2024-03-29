from aiogram import types, F, Router
from core.keyboards.main_kb import get_inline_main, get_reply_main
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os
import logging
import docker


router = Router()


@router.message(F.text.lower() == "в главное меню")
@router.message(Command(commands=['start', 'help']))
async def start_cmd_handler(message: Message, state: FSMContext) -> None:
    try:
        await message.reply("Вас приветствует Экспо-Бот! \n<b>v.1.4 - от 29.01.24</b>", reply_markup=get_inline_main()
                            )
        await message.answer("<b>✅ Выберете действие:</b>", reply_markup=get_reply_main()
                             )
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)
        # Cancel state and inform user about it
        await state.clear()
    except Exception as e:
        await message.reply(f'Походу что-то сломалось\n {e}', )


@router.message(Command('restart'))
async def restart_bot(message: types.Message):
    # await message.reply(f'Выполняется перезагрузка БОТА\n')
    # await dp.stop_polling()
    # subprocess.call([sys.executable, os.path.join(os.getcwd(), __file__)])
    # # await bot.close()
    # asyncio.create_task(zkt_sql_list.sql_export())
    # await asyncio.sleep(1)
    # await main()

    await message.reply(f'Выполняется перезагрузка БОТА\n')
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    docker_client.close()
