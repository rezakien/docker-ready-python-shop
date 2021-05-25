from datetime import datetime

from aiogram import types
from sqlalchemy import Column, Integer, String, Sequence, JSON, DateTime, Boolean, sql, ForeignKey

from utils.db.models.user import User
from utils.db.database import db


class Order(db.Model):
    __tablename__ = 'order'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    sum = Column(Integer)
    purchase_time = Column(DateTime)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    successful = Column(Boolean, default=False)
    datetime = Column(DateTime, default=datetime.now)

    @staticmethod
    async def get_orders():
        current = types.User.get_current()
        user = await User.get_user(current.id)
        return await Order.query.where(Order.user_id == user.id).order_by(Order.datetime.desc()).gino.all()