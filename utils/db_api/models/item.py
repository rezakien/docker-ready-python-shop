from sqlalchemy import (Column, Integer, String, Sequence, ForeignKey)
from sqlalchemy import sql
from utils.db_api.database import db


class Item(db.Model):
    __tablename__ = 'item'
    query: sql.Select

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)

    category_id = db.Column(Integer, ForeignKey('category.id'))

    def __repr__(self):
        return f"""
Товар № {self.id} - "{self.name}"
Цена: {self.price}
"""
