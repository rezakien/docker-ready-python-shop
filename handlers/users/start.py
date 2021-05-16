import random

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot
from utils.db_api.database import DBCommands

db = DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    chat_id = message.from_user.id
    referral = message.get_args()
    id = await db.add_new_user(referral=referral)

    count_users = await db.count_users()

    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Записал в базу! "

    bot_username = (await bot.me).username
    id_referral = id
    bot_link = f"https://t.me/{bot_username}?start={id_referral}".format(
        bot_username=bot_username,
        id_referral=id_referral
    )
    balance = await db.check_balance()
    text += f"""Сейчас в базе {count_users} человек! 
Ваша реферальная ссылка: {bot_link}
Проверить рефералов можно по команде: /referrals
Ваш баланс: {balance} монет.
Добавить монет: /add_money
"""
    await message.answer(text)


@dp.message_handler(commands=["referrals"])
async def check_referrals(message: types.Message):
    referrals = await db.check_referrals()
    if referrals != '':
        text = "Ваши рефералы:\n" + referrals
    else:
        text = "У вас нет рефераллов."
    await message.answer(text)


@dp.message_handler(commands=["add_money"])
async def add_money(message: types.Message):
    random_amount = random.randint(1, 1000)
    await db.add_money(random_amount)
    balance = await db.check_balance()
    text = "Вам было добавлено {money} монет.\nТеперь ваш баланс: {balance}".format(
        money=random_amount,
        balance=balance
    )
    await message.answer(text)
