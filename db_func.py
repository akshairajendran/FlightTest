__author__ = 'arajendran'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
import datetime

from gen_db import Base, Users, Flights

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

def add_flight(user, airport_from, airport_to, date, carrier, flight_no):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker()
    session = DBSession()

    if user is None or airport_from is None or airport_to is None or date is None or flight_no is None:
        return "Please enter all information"
    else:
        q = session.query(Users).filter(Users.username == user).first()
        date_format = datetime.datetime.strptime(date, '%Y-%M-%d').date()
        new_flight = Flights(airport_from = airport_from, airport_to = airport_to, date = date_format, carrier = carrier, flight_no = flight_no)
        new_flight.user = q
        session.add(new_flight)
        session.commit()
        return None

def display_flights(user, binary):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    if binary == 2:
        all_flights = session.query(Flights).filter(Flights.user == q).all()
    else:
        all_flights = session.query(Flights).filter(Flights.user == q, Flights.binary == binary).all()
    list = [[all_flights[i].airport_from, all_flights[i].airport_to, all_flights[i].date, all_flights[i].carrier, all_flights[i].flight_no] for i in range(len(all_flights))]
    return list
