from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, ForeignKey, DateTime, sql, Text, String
from utils.db_api.database import db


class Config(db.Model):
    __tablename__ = 'config'
    query: sql.Select

    id = Column(Integer, Sequence('config_id_seq'), primary_key=True)
    param = Column(String(255))
    value = Column(Text)
    datetime = Column(DateTime, default=datetime.now)
