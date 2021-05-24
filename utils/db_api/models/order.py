from datetime import datetime

from sqlalchemy import Column, Integer, String, Sequence, JSON, DateTime, Boolean, sql
from utils.db_api.database import db


class Order(db.Model):
    __tablename__ = 'order'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    sum = Column(Integer)
    purchase_time = Column(DateTime)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    successful = Column(Boolean, default=False)
    datetime = Column(DateTime, default=datetime.now)
