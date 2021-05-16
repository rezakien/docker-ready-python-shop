from gino import Gino

from aiogram import types
from asyncpg import Connection, Record, UniqueViolationError
from loader import bot, db


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat_id, username, full_name, referral) VALUES ($1, $2, $3, $4) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_REFERRALS = "SELECT chat_id FROM users WHERE referral=" \
                      "(SELECT id from users WHERE chat_id = $1)"
    CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    UPDATE_MONEY = "UPDATE users SET balance = balance + $1 WHERE chat_id=$2"

    async def add_new_user(self, referral=None):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = (chat_id, username, full_name)

        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        return await self.pool.fetchval(self.COUNT_USERS)

    async def get_id(self):
        user_id = types.User.get_current().id
        return await self.pool.fetchval(self.GET_ID, user_id)

    async def check_referrals(self):
        user_id = types.User.get_current().id
        rows = await self.pool.fetch(self.CHECK_REFERRALS, user_id)
        text = ""
        for key, row in enumerate(rows):
            chat = await bot.get_chat(row["chat_id"])
            user_link = chat.get_mention(as_html=True)
            text += str(key + 1) + ". " + user_link + "\n"
        return text

    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def add_money(self, money):
        command = self.UPDATE_MONEY
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, money, user_id)