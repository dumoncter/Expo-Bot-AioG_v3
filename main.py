import asyncio
from aiogram import Router
from core.handlers.zkt import zkt_sql_list, zkt
from core.handlers.zywall import zywall
from core.handlers.nettools import net_tols_main
from create_bot import dp, Bot
from core import start_bot

loop = asyncio.get_event_loop()
router = Router()
admin_users = [885923626]
# # admin_users = [885923626, 274395383, 91440123]


async def bot_start(bot: Bot):
    for user_id in admin_users:
        await bot.send_message(chat_id=user_id, text=f"🤖 <b>Бот запущен!</b>")
        await asyncio.sleep(1)


async def bot_stop(bot: Bot):
    for user_id in admin_users:
        await bot.send_message(chat_id=user_id, text=f"⚠ <b>Бот остановлен!</b>")
        await asyncio.sleep(1)


async def main():
    await dp.start_polling(Bot,
                           skip_updates=True,
                           )


def start():
    dp.startup.register(bot_start)
    asyncio.set_event_loop(loop)
    dp.include_routers(
        start_bot.router,
        net_tols_main.router,
        zkt.router,
        zywall.router,

    )
    try:
        dp.shutdown.register(bot_stop)
        loop.run_until_complete(main())
        loop.run_until_complete(zkt_sql_list.sql_export())
        Bot.delete_webhook(drop_pending_updates=True)
        loop.create_task(dp.start_polling())
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    start()
