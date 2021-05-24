from datetime import datetime

from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey, DateTime, Boolean)
from sqlalchemy import sql
from utils.db_api.database import db
from utils.db_api.models.item import Item


# def default_name_code(context):
#     return "c_" + '_'.join(context.get_current_parameters()['name'].split())


class Category(db.Model):
    __tablename__ = 'category'
    query: sql.Select

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(100))
    parent_id = Column(Integer, ForeignKey('category.id'))
    datetime = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return "<Category(id='{}', name='{}')>".format(
            self.id, self.name)

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
