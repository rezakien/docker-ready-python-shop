import logging

import asyncio
import logging

import exceptions
from constants.lang import *

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode

from config import MY_ID, BOT_TOKEN
from keyboard import get_keyboard

logging.basicConfig(level=logging.INFO)

# loop = asyncio.get_running_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


def auth(func):
    async def wrapper(message):
        print(message.from_user.id)
        if message.from_user.id != MY_ID:
            return await message.answer('Access Denied', reply=False)
        return await func(message)

    return wrapper


@dp.message_handler(commands=['start'])
@auth
async def process_start_command(message: Message):
    msg = text(START_MESSAGE['ru'],
               START_MESSAGE['uz'],
               '\n\n' + CHOOSE_LANGUAGE['ru'],
               CHOOSE_LANGUAGE['uz']
               , sep='\n')
    await message.answer(msg, reply_markup=get_keyboard())


@dp.message_handler(Text(equals=["O'zbekcha", 'Русский']))
async def show_menu(message: Message):
    await message.answer(f"Вы выбрали {message.text}. Спасибо!", reply_markup=get_keyboard(False))


@dp.message_handler(commands=['help'])
@auth
async def process_help_command(message: Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/start', '/help', '/cart', '/contact', sep='\n')
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['enter_admin'], commands_prefix='~')
@auth
async def admin_message(message: Message):
    await message.answer('Enter password')


@dp.message_handler(commands=["/create_poll"])
@auth
async def test(message: Message):
    await message.answer("Нажмите на кнопку ниже и создайте викторину!", reply_markup=get_keyboard('poll'))


if __name__ == '__main__':
    from handlers import dp, send_to_admin

    executor.start_polling(dp, on_startup=send_to_admin)
