from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql, String
from utils.db.database import db


class Price(db.Model):
    __tablename__ = 'price'
    query: sql.Select

    id = Column(Integer, Sequence('price_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    min_quantity = Column(Integer)
    max_quantity = Column(Integer)
    price = Column(Integer)
    datetime = Column(DateTime, default=datetime.now)
