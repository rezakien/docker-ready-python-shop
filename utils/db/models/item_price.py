from sqlalchemy import Column, Integer, Sequence, ForeignKey, sql
from utils.db.database import db


class ItemPrice(db.Model):
    __tablename__ = 'order_price'
    query: sql.Select

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    price_id = Column(Integer, ForeignKey('price.id'))
    price = Column(Integer)
