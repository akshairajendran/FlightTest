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

    q = session.query(Users).filter(Users.username == user).first()
    if user == "":
        return "Please enter a valid username"
    if pwd == "":
        return "Please enter a valid password"
    if hasattr(q, 'username'):
        return "Username already exists"
    else:
        new_user = Users(username=user,password=sha256_crypt.encrypt(pwd))
        session.add(new_user)
        session.commit()
        return None