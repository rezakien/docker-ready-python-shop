from datetime import datetime

from aiogram import types
from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql, and_, or_

from utils.db import User, Item, Price
from utils.db.database import db


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
                return await cart_item.update(quantity=cart_item.quantity + kwargs["quantity"]).apply()
        else:
            if cart_item is not None:
                return await cart_item.delete()
            else:
                return False

    @staticmethod
    async def get_cart():
        current = types.User.get_current()
        user = await User.get_user(current.id)
        return await Cart.query.where(Cart.user_id == user.id).order_by(Cart.datetime.desc()).gino.all()

    @staticmethod
    async def get_cart_sum():
        current = types.User.get_current()
        user = await User.get_user(current.id)
        cart_items = await Cart.query.where(Cart.user_id == user.id).gino.all()
        summary = 0
        for cart_item in cart_items:
            item_prices = await Price.query.where(Price.item_id == cart_item.item_id).order_by(Price.min_quantity.asc()).gino.all()
            price = None
            for item_price in item_prices:
                if cart_item.quantity >= item_price.min_quantity and cart_item.quantity < item_price.max_quantity:
                    price = item_price.price
                    break
                elif cart_item.quantity < item_price.min_quantity:
                    item = await Item.get_item(cart_item.item_id)
                    price = item.price
                    break
            summary += price * cart_item.quantity
        return summary

    @staticmethod
    async def get_cart_items():
        current = types.User.get_current()
        user = await User.get_user(current.id)
        cart_items = await Cart.query.where(Cart.user_id == user.id).gino.all()
        return cart_items

    @staticmethod
    async def get_cart_item(item_id):
        current = types.User.get_current()
        user = await User.get_user(current.id)
        conditions = [
            Cart.user_id == user.id,
            Cart.item_id == item_id,
        ]
        cart_item = await Cart.query.where(and_(*conditions)).gino.first()
        return cart_item

    @staticmethod
    async def clear_cart():
        cart_items = await Cart.get_cart_items()
        for cart_item in cart_items:
            await cart_item.delete()
