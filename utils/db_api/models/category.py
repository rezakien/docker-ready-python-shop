from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey, Text)
from sqlalchemy import sql
from utils.db_api.database import db


class Category(db.Model):
    __tablename__ = 'category'
    query: sql.Select

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(50))
    photo = Column(String(250))
    description = Column(Text)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return f"""
Категория "{self.name}"
Описание: {self.description}
"""
