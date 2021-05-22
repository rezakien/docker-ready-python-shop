from importlib._common import _

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_keyboard import menu_keyboard
from loader import dp, _
from utils.db_api.database import DBCommands

db = DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    referral = message.get_args()
    user = await db.add_new_user(referral=referral)

    text = _("Нажмите кнопку:")
    await message.answer(text=text, reply_markup=menu_keyboard)
