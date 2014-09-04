__author__ = 'arajendran'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt

from gen_db import Base, Users

def add_user(user,pwd):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_user = Users(username=user,password=sha256_crypt.encrypt(pwd))
    session.add(new_user)
    session.commit()
