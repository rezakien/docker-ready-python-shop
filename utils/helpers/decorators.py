from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from loader import _
from utils.db.models import User


def admin_sign_in_message(func):
    async def wrapper(message: Message):
        user_signed_in = await User.user_signed_in(check_admin=True)
        if not user_signed_in:
            text = _("⛔️ Доступ в админ панель только у администраторов.")
            await message.answer(text=text)
        else:
            return await func(message)
    return wrapper


def admin_sign_in_callback(func):
    async def wrapper(call: CallbackQuery, callback_data: dict):
        user_signed_in = await User.user_signed_in(check_admin=True)
        if not user_signed_in:
            text = _("⛔️ Доступ в админ панель только у администраторов.")
            await call.message.answer(text=text)
        else:
            return await func(call, callback_data)
    return wrapper


def user_sign_in_message(func):
    async def wrapper(message: Union[Message, ContentType.LOCATION, ContentType.CONTACT]):
        user_signed_in = await User.user_signed_in()
        if not user_signed_in:
            text = _("Выполнить действие невозможно. Введите /start, чтобы войти.")
            await message.answer(text=text)
        else:
            return await func(message)
    return wrapper


def user_sign_in_message_state(func):
    async def wrapper(message: Union[Message, ContentType.LOCATION, ContentType.CONTACT], state: FSMContext):
        user_signed_in = await User.user_signed_in()
        if not user_signed_in:
            text = _("Выполнить действие невозможно. Введите /start, чтобы войти.")
            await message.answer(text=text)
        else:
            return await func(message, state)
    return wrapper


def user_sign_in_callback(func):
    async def wrapper(call: CallbackQuery, callback_data: dict):
        user_signed_in = await User.user_signed_in()
        if not user_signed_in:
            text = _("Выполнить действие невозможно. Введите /start, чтобы войти.")
            await call.message.answer(text=text)
        else:
            return await func(call, callback_data)
    return wrapper
