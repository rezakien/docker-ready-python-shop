from aiogram import executor
from handlers import dp

from loader import bot
from config import ADMIN_ID


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(ADMIN_ID, "bot-is-started")


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
