from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command, CommandHelp

from keyboards.inline.admin.menu import get_admin_menu
from loader import dp, _
from utils.helpers.decorators import admin_sign_in_message


@dp.message_handler(Command("admin"))
@admin_sign_in_message
async def menu_orders_handler(message: Message):
    reply_markup = get_admin_menu()
    return await message.answer(text="Вы вошли в админ панель.\n"
                                     "Введите /help для отображения инструкции."
                                , reply_markup=reply_markup)


@dp.message_handler(CommandHelp())
@admin_sign_in_message
async def menu_orders_handler(message: Message):
    return await message.answer(text="Это админ панель Ver.1. \n\nПока что возможнен только просмотр записей.")
