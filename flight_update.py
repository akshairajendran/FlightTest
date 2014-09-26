__author__ = 'arajendran'

import sys
from suds import null, WebFault
from suds.client import Client
import logging
import time
import datetime

#open config file and get username and api key
f = open('config.txt','r')
credentials = [line[line.index(':')+1:len(line)].strip() for line in f]

#credentials
username = credentials[0]
apiKey = credentials[1]
url = 'http://flightxml.flightaware.com/soap/FlightXML2/wsdl'

#setup logging and api
logging.basicConfig(level=logging.INFO)
api = Client(url, username=username, password=apiKey)

#set endpoint
def reg_endpoint(endpoint = 'http://akshairajendran.com/flightserve'):
    api.service.RegisterAlertEndpoint(endpoint,'json/post')

#set alert for new flight
def set_alert(airport_from, airport_to, date, carrier, flight_no):
    flight_codes = {'Delta':'DAL', 'United': 'UAL', 'Southwest':'SWA', 'AirTran':'TRS', 'Alaska':'ASA', 'American':'AAL',
                    'Frontier':'FFT', 'Hawaiian':'HAL','JetBlue':'JBU','Spirit':'NKS','US Airways':'AWE', 'Virgin':'VRD' }
    carrier_code = flight_codes[carrier]
    ident = str(carrier_code) + str(flight_no)
    if check_flight(airport_from, airport_to, date, carrier, flight_no):
        try:
            api.service.SetAlert(alert_id=0,ident=ident,origin=airport_from,destination=airport_to,date_start=to_epoch(date),date_end=to_epoch(date),channels="{16 e_filed e_departure e_arrival e_diverted e_cancelled}",max_weekly=1000)
            return True
        except:
            print "Couldn't add"
            return False
    else:
        return False
#match alert
def match_alert(date=None,carrier=None,flight_no=None,airport_from=None,identifier=None):
    if identifier == None:
        flight_codes = {'Delta':'DAL', 'United': 'UAL', 'Southwest':'SWA', 'AirTran':'TRS', 'Alaska':'ASA', 'American':'AAL',
                        'Frontier':'FFT', 'Hawaiian':'HAL','JetBlue':'JBU','Spirit':'NKS','US Airways':'AWE', 'Virgin':'VRD' }
        carrier_code = flight_codes[carrier]
        ident = str(carrier_code) + str(flight_no)
    else:
        ident = identifier
    all_alerts = get_alert()
    match = [i for i in all_alerts[1] if (i.user_ident == ident or i.ident == ident) and i.date_start == to_epoch(date) and i.origin[1:] == airport_from]
    return match[0]

#delete alert
def del_alert(date=None, carrier=None, flight_no=None, airport_from=None,identifier=None):
    match = match_alert(date=date,carrier=carrier,flight_no=flight_no,airport_from=airport_from,identifier=identifier)
    alert_id = match.alert_id
    try:
        api.service.DeleteAlert(alert_id)
        return True
    except:
        return False

#check all alerts
def get_alert():
    return api.service.GetAlerts()

#get flight info
def check_flight(airport_from, airport_to, date, carrier, flight_no):
    flight_codes = {'Delta':'DAL', 'United': 'UAL', 'Southwest':'SWA', 'AirTran':'TRS', 'Alaska':'ASA', 'American':'AAL',
                    'Frontier':'FFT', 'Hawaiian':'HAL','JetBlue':'JBU','Spirit':'NKS','US Airways':'AWE', 'Virgin':'VRD' }
    carrier_code = flight_codes[carrier]
    ident = str(carrier_code) + str(flight_no)
    results = api.service.AirlineFlightSchedules(to_epoch(date),to_epoch(date)+86400,airport_from,airport_to,carrier_code,flight_no,15)

    if len(results) < 2:
        return False
    else:
        return True

#dealing w epoch seconds
def to_epoch(date):
    pattern = '%Y-%m-%d'
    epoch = int(time.mktime(time.strptime(date, pattern)))
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset = - (time.altzone if is_dst else time.timezone)
    return epoch + utc_offset

def from_epoch(date):
    return datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')

#get flight info from fa_id
def flight_info(fa_id):
    return api.service.FlightInfoEx(fa_id,10,0)