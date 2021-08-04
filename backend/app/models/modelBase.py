from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, DateTime
from datetime import datetime

class Base(object):
    created = Column(DateTime, default=datetime.utcnow)

ModelBase = declarative_base(cls=Base)
