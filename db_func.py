__author__ = 'arajendran'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
import datetime
import HTML
from flight_update import from_epoch

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

def add_flight(user, airport_from, airport_to, date, carrier, flight_no, recipient):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    date_format = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    new_flight = Flights(airport_from = airport_from, airport_to = airport_to, date = date_format, carrier = carrier, flight_no = flight_no, recipient = recipient)
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
        list = [[all_flights[i].airport_from, all_flights[i].airport_to, all_flights[i].date, all_flights[i].carrier, all_flights[i].flight_no] for i in range(len(all_flights))]
    elif binary == 1:
        all_flights = session.query(Flights).filter(Flights.user == q, Flights.binary == binary).all()
        list = [[all_flights[i].airport_from, all_flights[i].airport_to, all_flights[i].date, all_flights[i].carrier, all_flights[i].flight_no] for i in range(len(all_flights))]
    else:
        all_flights = session.query(Flights).filter(Flights.user == q, Flights.binary == binary).all()
        list = [[all_flights[i].airport_from, all_flights[i].airport_to, all_flights[i].date, all_flights[i].carrier, all_flights[i].flight_no, all_flights[i].recipient, '<a href="/del_flight?flightid='+str(all_flights[i].id)+'">Delete</a>'] for i in range(len(all_flights))]
    session.commit()
    return list


def del_flight(user, flightid):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    flight = session.query(Flights).filter(Flights.user == q, Flights.id == flightid).delete()
    session.commit()
    return

def check_flight(user=None, date=None, carrier=None, flight_no=None, flightid=None):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()

    if flightid != None:
        flight = session.query(Flights).filter(Flights.user == q, Flights.id == flightid).first()
        date = flight.date
        carrier = flight.carrier
        flight_no = flight.flight_no
    else:
        date = datetime.datetime.strptime(date, '%Y-%M-%d').date()
    query = session.query(Flights).filter(Flights.user != q, Flights.date == date, Flights.carrier == carrier, Flights.flight_no == flight_no).first()
    if hasattr(query, 'date'):
        return True
    else:
        return False

def check_myflight(user=None, date=None, carrier=None, flight_no=None, flightid=None):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()

    if flightid != None:
        flight = session.query(Flights).filter(Flights.user == q, Flights.id == flightid).first()
        date = flight.date
        carrier = flight.carrier
        flight_no = flight.flight_no
    else:
        date = datetime.datetime.strptime(date, '%Y-%M-%d').date()
    query = session.query(Flights).filter(Flights.user == q, Flights.date == date, Flights.carrier == carrier, Flights.flight_no == flight_no).first()
    if hasattr(query, 'date'):
        return True
    else:
        return False

def get_attr(attr, flightid):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    flight = session.query(Flights).filter(Flights.id == flightid).first()

    if attr == 'date':
        return flight.date.strftime('%Y-%m-%d')
    elif attr == 'carrier':
        return flight.carrier
    elif attr == 'flight_no':
        return flight.flight_no
    elif attr == 'recipient':
        return flight.recipient
    else:
        return False

def get_allfid(date_in, ident):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    flight_codes = {'Delta':'DAL', 'United': 'UAL', 'Southwest':'SWA', 'AirTran':'TRS', 'Alaska':'ASA', 'American':'AAL',
                    'Frontier':'FFT', 'Hawaiian':'HAL','JetBlue':'JBU','Spirit':'NKS','US Airways':'AWE', 'Virgin':'VRD' }
    inv_fc = {v:k for k, v in flight_codes.items()}
    air_code = ident[:3]
    #we've pulled out the airline and flight_no
    airline = inv_fc[air_code]
    flight_no = ident[3:]

    #we need to format the date we'll be getting in epoch form to just a date
    date = datetime.datetime.strptime(from_epoch(date_in),'%Y-%m-%d %H:%M:%S').date()

    #now let's query all flights matching the departure date, airline and flight no
    flights = session.query(Flights).filter(Flights.date == date, Flights.carrier == airline, Flights.flight_no == flight_no).all()

    #append to this list the id of each object in flights
    ids = [i.id for i in flights]
    return ids