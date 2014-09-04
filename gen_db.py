__author__ = 'arajendran'

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import PasswordType


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(200),nullable=False)

engine = create_engine('sqlite:///flighttest.db')

if __name__ == '__main__':
    Base.metadata.create_all(engine)