from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql, String
from utils.db.database import db


class Price(db.Model):
    __tablename__ = 'price'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    name = Column(String(255))
    min_quantity = Column(Integer)
    max_quantity = Column(Integer)
