import asyncio

from aiogram import executor


from loader import bot
from config import ADMIN_ID
from utils.db_api.database import create_db


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    # await asyncio.sleep(10)
    await create_db()
    await bot.send_message(ADMIN_ID, "Я запущен /start")


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
