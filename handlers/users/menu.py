from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    pass


async def list_categories(message: Union[types.Messagem, types.CallbackQuery], **kwargs)
    markup = await categories_keyboard()