__author__ = 'arajendran'

import sys
from suds import null, WebFault
from suds.client import Client
import logging

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
    
