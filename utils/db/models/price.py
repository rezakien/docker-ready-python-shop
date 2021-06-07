from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql, String
from utils.db.database import db


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
