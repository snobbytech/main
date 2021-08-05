from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, DateTime
from datetime import datetime


# TODO: make a basic implementation of populateFromDict here, versus in each of the subclasses.
# Same thing with a validate.
# I just don't remember how to override it, but let's do all that software engineering LATERRR
class Base(object):
    created = Column(DateTime, default=datetime.utcnow)

ModelBase = declarative_base(cls=Base)
