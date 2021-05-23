from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_keyboard import menu_keyboard
from keyboards.inline.lang_keyboard import lang_keyboard
from loader import dp, _
from utils.db_api.database import DBCommands

db = DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = types.User.get_current()
    referral = message.get_args()
    user_exists = await db.get_user(user.id)
    text = _("Нажмите кнопку:")
    if user_exists:
        await message.answer(text=text, reply_markup=menu_keyboard)
    else:
        await db.add_new_user(referral=referral)
        await message.answer(text=text, reply_markup=lang_keyboard)
