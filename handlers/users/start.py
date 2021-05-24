from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_keyboard import get_menu_keyboard
from keyboards.inline.lang_keyboard import get_lang_keyboard
from loader import dp, _
from utils.db_api.models.user import User


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = types.User.get_current()
    referral = message.get_args()
    user_db = await User.get_user(user.id)
    text = _("Нажмите кнопку:")
    if user_db is None:
        await User.create_user(referral=referral)
        await message.answer(text=text, reply_markup=get_lang_keyboard())
    else:
        await message.answer(text=text, reply_markup=get_menu_keyboard(user_db.language))
