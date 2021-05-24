from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql
from utils.db.database import db


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    quantity = Column(Integer, default=0)
    datetime = Column(DateTime, default=datetime.now)
