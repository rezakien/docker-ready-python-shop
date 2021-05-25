from datetime import datetime

from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, DateTime, Boolean)
from sqlalchemy import sql
from utils.db.database import db
from aiogram import types
from loader import Bot


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(10))
    full_name = Column(String(100))
    username = Column(String(50))
    admin = Column(Boolean)
    password = Column(String(255))
    referral = Column(Integer)
    datetime = Column(DateTime, default=datetime.now)
    query: sql.Select

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}', language='{}')>".format(
            self.id, self.full_name, self.username, self.language)

    @staticmethod
    async def user_signed_in(check_admin=False):
        get_current = types.User.get_current()
        user = await User.get_user(get_current.id)
        if user:
            if check_admin:
                if user.admin:
                    return True
                else:
                    return False
            return True
        else:
            return False

    @staticmethod
    async def get_user(user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def create_user(referral=None):
        user = types.User.get_current()
        old_user = await User.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name

        # хардкодим
        admin_ids = [283989538]
        if user.id in admin_ids:
            new_user.admin = True

        if referral:
            new_user.referral = int(referral)
        await new_user.create()
        return new_user

    @staticmethod
    async def set_language(language):
        user_id = types.User.get_current().id
        user = await User.get_user(user_id)
        return await user.update(language=language).apply()

    async def count_users(self) -> int:
        total = await db.func.count(self.id).gino.scalar()
        return total

    @staticmethod
    async def check_referrals():
        bot = Bot.get_current()
        user_id = types.User.get_current().id

        user = await User.query.where(User.user_id == user_id).gino.first()
        referrals = await User.query.where(User.referral == user.id).gino.all()

        return ", ".join([
            f"{num + 1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
            for num, referral in enumerate(referrals)
        ])
