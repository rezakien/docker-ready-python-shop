from datetime import datetime

from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey, DateTime, Boolean, and_, or_)
from sqlalchemy import sql

from utils.db.models.price import Price
from utils.db.database import db

from pathlib import Path
import logging

# def default_name_code(context):
#     return "item_" + context.get_current_parameters()['name']


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
        prices = ''
        if item_prices is not None:
            prices += '\n\nЦены за товар:\n'
            for item_price in item_prices:
                prices += f"{item_price}\n"
        return "{item}{prices}".format(item=self, prices=prices)

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
        logging.info(price_max)
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
        photo = Path(__file__).parents[3] / 'images' / self.photo
        photo = str(photo.resolve())
        photo = open(photo.encode('utf-8'), 'rb')
        return photo
