from datetime import datetime

from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey, DateTime, Boolean)
from sqlalchemy import sql
from utils.db.database import db
from utils.db.models.item import Item


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
