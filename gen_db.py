__author__ = 'arajendran'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

from sqlalchemy.types import Date


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(200),nullable=False)

class Flights(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users, backref=backref('flights', uselist=True))
    airport_from = Column(String(3))
    airport_to = Column(String(3))
    date = Column(Date)
    carrier = Column(String(50))
    flight_no = Column(Integer)
    recipient = Column(String(100))
    ident = Column(String(10))
    fa_flightid = Column(String(50))
    binary = Column(Integer, default = 0)

engine = create_engine('sqlite:///flighttest.db')

if __name__ == '__main__':
    Base.metadata.create_all(engine)