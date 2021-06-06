from datetime import datetime

from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey, DateTime, Boolean, and_)
from sqlalchemy import sql

from utils.db.models.price import Price
from utils.db.database import db

from pathlib import Path


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

    def __repr__(self):
        return "Товар: <b>{name}</b>".format(name=self.name)

    @staticmethod
    async def all_items():
        return await Item.query.gino.all()

    @staticmethod
    async def get_item(id_item):
        return await Item.get(id_item)

    async def get_price(self, quantity):
        conditions = [
            Price.item_id == self.id,
            Price.min_quantity >= quantity,
            Price.max_quantity < quantity,
        ]
        return await Price.query.where(and_(*conditions)).gino.one()

    async def get_photo(self):
        photo = Path(__file__).parents[3] / 'images' / self.photo
        photo = str(photo.resolve())
        photo = open(photo.encode('utf-8'), 'rb')
        return photo
