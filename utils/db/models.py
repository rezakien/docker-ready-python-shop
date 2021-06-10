from datetime import datetime
import logging

from sqlalchemy import (Column, Integer, String, Sequence, BigInteger, DateTime, Boolean, ForeignKey, Text, JSON, and_,
                        FLOAT)
from sqlalchemy import sql
from utils.db.database import db
from aiogram import types
from loader import Bot
from pathlib import Path


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

        if new_user.admin is not True:
            admin_usernames = ['rezakien', 'dli_abdurakhmanov']
            if user.username in admin_usernames:
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

    @staticmethod
    async def get_lang(user_id):
        user = await User.get_user(user_id)
        if user:
            return user.language


class Category(db.Model):
    __tablename__ = 'category'
    query: sql.Select

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(100))
    parent_id = Column(Integer, ForeignKey('category.id'))
    datetime = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return "Категория: <b>{}</b>".format(self.name)

    @staticmethod
    async def all_parents():
        return await Category.query.where(Category.parent_id.is_(None)).gino.all()

    @staticmethod
    async def all_subcategories():
        return await Category.query.where(Category.parent_id.isnot(None)).gino.all()

    @staticmethod
    async def all_subcategories_of_category(parent_id):
        return await Category.query.where(Category.parent_id == parent_id).gino.all()

    @staticmethod
    async def all_items_of_category(category_id):
        return await Item.query.where(Item.category_id == category_id).gino.all()

    @staticmethod
    async def count_items(category_id):
        return await db.select([db.func.count()]).where(Item.category_id == category_id).gino.scalar()

    @staticmethod
    async def get_parent_category(parent_id):
        return await Category.query.where(Category.id == parent_id).gino.first()

    @staticmethod
    async def create_category(**kwargs):
        return await Category(**kwargs).create()


class Price(db.Model):
    __tablename__ = 'price'
    query: sql.Select

    def __repr__(self):
        add_text = ""
        if self.max_quantity is not None:
            add_text = f"до <b>{self.max_quantity:,}кг</b>"
        return f"<b>{self.price:,} сум</b> от <b>{self.min_quantity:,}кг</b> {add_text}".strip()

    id = Column(Integer, Sequence('price_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    min_quantity = Column(Integer)
    max_quantity = Column(Integer)
    price = Column(Integer)
    datetime = Column(DateTime, default=datetime.now)


class Item(db.Model):
    __tablename__ = 'item'
    query: sql.Select

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50))
    category_id = Column(Integer, ForeignKey('category.id'))
    price = Column(Integer)
    photo = Column(String(250))
    datetime = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    async def get_item_text(self):
        item_prices = await Price.query.where(Price.item_id == self.id).order_by(Price.price.desc()).gino.all()
        item_cart = await Cart.query.where(Cart.item_id == self.id).gino.first()
        prices = ''
        added_to_cart = ''
        if item_prices is not None:
            prices += '\n\nЦены за товар:\n'
            for item_price in item_prices:
                prices += f"{item_price}\n"
        if item_cart is not None:
            added_to_cart = "\nДобавлено в корзину в объеме {item_quantity:,} кг. ✅ ".format(
                item_quantity=item_cart.quantity)
        return "{item}{prices}{added_to_cart}".format(item=self, prices=prices, added_to_cart=added_to_cart)

    def __repr__(self):
        return "Товар: <b>{name}</b>".format(name=self.name)

    @staticmethod
    async def all_items():
        return await Item.query.gino.all()

    @staticmethod
    async def get_item(id_item):
        return await Item.get(id_item)

    async def get_price(self, quantity):
        max_price = await db.select([db.func.max(Price.min_quantity)]).select_from(Price).where(
            Price.item_id == self.id).gino.scalar()

        cond_max = [
            Price.item_id == self.id,
            Price.min_quantity == max_price,
            Price.min_quantity <= quantity
        ]

        price_max = await Price.query.where(and_(*cond_max)).gino.first()
        if price_max is not None:
            return int(price_max.price)
        else:
            cond = [
                Price.item_id == self.id,
                Price.min_quantity <= quantity,
                Price.max_quantity > quantity
            ]
            price = await Price.query.where(and_(*cond)).gino.first()
            if price is None:
                return int(self.price)
            else:
                return int(price.price)

    async def get_photo(self):
        photo = Path(__file__).parents[2] / 'images' / self.photo
        photo = str(photo.resolve())
        photo = open(photo.encode('utf-8'), 'rb')
        return photo


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
                if kwargs["quantity"] >= 100:
                    return {
                        "message": await Cart(**kwargs).create(),
                        "success": True
                    }
                else:
                    return {
                        "message": "ERROR_CAPACITY",
                        "success": False
                    }
            else:
                return {
                    "message": await cart_item.update(quantity=cart_item.quantity + kwargs["quantity"]).apply(),
                    "success": True
                }
        else:
            if cart_item is not None:
                return {
                    "message": await cart_item.delete(),
                    "success": True
                }
            else:
                return {
                    "message": "UNKNOWN_ERROR",
                    "success": False
                }

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
            item = await Item.get_item(cart_item.item_id)
            price = await item.get_price(cart_item.quantity)
            summary += int(price) * cart_item.quantity
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


class Order(db.Model):
    __tablename__ = 'order'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    sum = Column(Integer)
    phone_number = Column(String(50))
    successful = Column(Boolean, default=False)
    canceled = Column(Boolean, default=False)
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    address = Column(Text)
    datetime = Column(DateTime, default=datetime.now)

    @staticmethod
    async def get_orders():
        current = types.User.get_current()
        user = await User.get_user(current.id)
        return await Order.query.where(Order.user_id == user.id).order_by(Order.datetime.desc()).gino.all()

    @staticmethod
    async def get_order_items(order_id, admin=False):
        current_user = types.User.get_current()
        user = await User.get_user(current_user.id)
        if admin is False:
            conditions = [
                OrderItem.order_id == order_id,
                OrderItem.user_id == user.id
            ]
        else:
            conditions = [
                OrderItem.order_id == order_id
            ]
        order_items = await OrderItem.query.where(and_(*conditions)).gino.all()
        return order_items

    @staticmethod
    async def cancel_order(order_id):
        current_user = types.User.get_current()
        user = await User.get_user(current_user.id)

        conditions = [
            Order.id == order_id,
            Order.user_id == user.id,
            Order.canceled is not False
        ]
        order = await Order.query.where(and_(*conditions)).gino.first()
        if order is not None:
            await order.update(canceled=True).apply()
        return order

    @staticmethod
    async def confirm_order(order_id):
        current_user = types.User.get_current()
        user = await User.get_user(current_user.id)

        conditions = [
            Order.id == order_id,
            Order.canceled is not False
        ]
        order = await Order.query.where(and_(*conditions)).gino.first()
        if order is not None:
            await order.update(successful=True).apply()
        return order

    @staticmethod
    async def new_orders():
        return await Order.query.where([Order.successful == False]).gino.all()

    @staticmethod
    async def successful_orders():
        return await Order.query.where([Order.successful == True]).gino.all()


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    price = Column(Integer)
    quantity = Column(Integer, default=0)
    summary = Column(Integer)
    datetime = Column(DateTime, default=datetime.now)


class Config(db.Model):
    __tablename__ = 'config'
    query: sql.Select

    id = Column(Integer, Sequence('config_id_seq'), primary_key=True)
    param = Column(String(255))
    value = Column(Text)
    datetime = Column(DateTime, default=datetime.now)
