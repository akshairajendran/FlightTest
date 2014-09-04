__author__ = 'arajendran'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt

from gen_db import Base, Users

def check_user(user,pwd):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    if hasattr(q, 'username'):
        if sha256_crypt.verify(pwd, q.password):
            return None
        else:
            return "Incorrect password"
    else:
        return "User does not exist"