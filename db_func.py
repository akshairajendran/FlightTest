__author__ = 'arajendran'

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
import datetime
from flight_update import from_epoch, match_alert

from gen_db import Base, Users, Flights, Recipients

def add_user(user,pwd):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    q = session.query(Users).filter(func.lower(Users.username) == func.lower(user)).first()
    if user == "":
        return "Please enter a valid username"
    if pwd == "":
        return "Please enter a valid password"
    if hasattr(q, 'username'):
        session.close()
        return "Username already exists"
    else:
        new_user = Users(username=user,password=sha256_crypt.encrypt(pwd))
        session.add(new_user)
        session.commit()
        session.close()
        return None

def check_user(user,pwd):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(func.lower(Users.username) == func.lower(user)).first()
    if hasattr(q, 'username'):
        if sha256_crypt.verify(pwd, q.password):
            session.close()
            return None
        else:
            session.close()
            return "Incorrect password"
    else:
        session.close()
        return "User does not exist"

def add_flight(user, airport_from, airport_to, date, carrier, flight_no, recipients):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    date_format = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    match = match_alert(date,carrier,flight_no,airport_from)
    ident = match.ident
    new_flight = Flights(airport_from = airport_from, airport_to = airport_to, date = date_format, carrier = carrier, flight_no = flight_no, ident=ident)
    new_flight.user = q
    session.add(new_flight)
    session.commit()
    flight = session.query(Flights).filter(Flights.user == q, Flights.airport_from == airport_from, Flights.airport_to == airport_to, Flights.date == date_format, Flights.carrier == carrier, Flights.flight_no == flight_no).first()
    for recip in recipients:
        new_recipient = Recipients(recipient = recip)
        new_recipient.flight = flight
        session.add(new_recipient)
        session.commit()
    session.close()
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
        list = [[all_flights[i].airport_from, all_flights[i].airport_to, all_flights[i].date, all_flights[i].carrier, all_flights[i].flight_no, '<a href="/rec_flight?flightid='+str(all_flights[i].id)+'">Recipients</a>', '<a href="/del_flight?flightid='+str(all_flights[i].id)+'">Delete</a>'] for i in range(len(all_flights))]
    session.commit()
    session.close()
    return list

def display_recipients(user, flight_id):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    all_recipients = session.query(Recipients).filter(Recipients.flight_id == flight_id).all()
    list = [[all_recipients[i].recipient] for i in range(len(all_recipients))]
    session.commit()
    session.close()
    return list

def del_flight(user, flightid):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    q = session.query(Users).filter(Users.username == user).first()
    flight = session.query(Flights).filter(Flights.user == q, Flights.id == flightid).delete()
    recipients = session.query(Recipients).filter(Recipients.flight_id == flightid).delete()
    session.commit()
    session.close()
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
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    query = session.query(Flights).filter(Flights.user != q, Flights.date == date, Flights.carrier == carrier, Flights.flight_no == flight_no).first()
    if hasattr(query, 'date'):
        session.close()
        return True
    else:
        session.close()
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
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    query = session.query(Flights).filter(Flights.user == q, Flights.date == date, Flights.carrier == carrier, Flights.flight_no == flight_no).first()
    if hasattr(query, 'date'):
        session.close()
        return True
    else:
        session.close()
        return False

def get_attr(attr, flightid):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    flight = session.query(Flights).filter(Flights.id == flightid).first()
    recipients = session.query(Recipients).filter(Recipients.flight_id == flightid).all()

    if attr == 'date':
        return flight.date.strftime('%Y-%m-%d')
    elif attr == 'carrier':
        return flight.carrier
    elif attr == 'flight_no':
        return flight.flight_no
    elif attr == 'recipient':
        return [recipients[i].recipient for i in range(len(recipients))]
    elif attr == 'user':
        return flight.user.username
    elif attr =='airport_from':
        return flight.airport_from
    else:
        return False

def get_allfid(date_in, ident,airport_from):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    # flight_codes = {'Delta':'DAL', 'United': 'UAL', 'Southwest':'SWA', 'AirTran':'TRS', 'Alaska':'ASA', 'American':'AAL',
    #                 'Frontier':'FFT', 'Hawaiian':'HAL','JetBlue':'JBU','Spirit':'NKS','US Airways':'AWE', 'Virgin':'VRD' }
    # inv_fc = {v:k for k, v in flight_codes.items()}
    # air_code = ident[:3]
    # #we've pulled out the airline and flight_no
    # airline = inv_fc[air_code]
    # flight_no = ident[3:]

    #we need to format the date we'll be getting in epoch form to just a date
    date = datetime.datetime.strptime(from_epoch(date_in),'%Y-%m-%d %H:%M:%S').date()

    #now let's query all flights matching the departure date, ident and departure airport
    flights = session.query(Flights).filter(Flights.date == date, Flights.ident == ident, Flights.airport_from == airport_from).all()

    #append to this list the id of each object in flights
    ids = [i.id for i in flights]
    return ids

def mark_old(ids):
    engine = create_engine('sqlite:///flighttest.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    session = DBSession()

    #take in a list of flight ids and switch their binaries, because they landed!
    for id in ids:
        flight = session.query(Flights).filter(Flights.id == id).first()
        flight.binary = 1
        session.commit()
    session.close()
    return