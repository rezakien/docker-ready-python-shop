from datetime import datetime

from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey, DateTime, Boolean)
from sqlalchemy import sql
from utils.db_api.database import db


# def default_name_code(context):
#     return "item_" + context.get_current_parameters()['name']


class Item(db.Model):
    __tablename__ = 'item'
    query: sql.Select

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    photo = Column(String(250))
    datetime = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return "Товар: <b>{}</b>" \
               "\nЦена: <b>{}</b> сум.".format(self.name, self.price)

    @staticmethod
    async def all_items():
        return await Item.query.gino.all()

    @staticmethod
    async def get_item(id_item):
        return await Item.get(id_item)

    @staticmethod
    async def create_item(**kwargs):
        return await Item(**kwargs).create()
