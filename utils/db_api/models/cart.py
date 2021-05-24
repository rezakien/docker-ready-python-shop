from datetime import datetime

from aiogram import types
from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql, and_

from utils.db_api import User
from utils.db_api.database import db


class Cart(db.Model):
    __tablename__ = 'cart'
    query: sql.Select

    id = Column(Integer, Sequence('cart_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    quantity = Column(Integer, default=0)
    datetime = Column(DateTime, default=datetime.now)

    @staticmethod
    async def create_update_item(**kwargs):
        conditions = [
            Cart.item_id == kwargs["item_id"],
            Cart.user_id == kwargs["user_id"]
        ]
        cart_item = await Cart.query.where(and_(*conditions)).gino.first()
        if kwargs["quantity"] > 0:
            if cart_item is None:
                return await Cart(**kwargs).create()
            else:
                return await cart_item.update(quantity=cart_item.quantity+kwargs["quantity"]).apply()
        else:
            if cart_item is not None:
                await cart_item.delete()

    @staticmethod
    async def get_cart():
        current = types.User.get_current()
        user = await User.get_user(current.id)
        return await Cart.query.where(Cart.user_id == user.id).order_by(Cart.datetime.desc()).gino.all()