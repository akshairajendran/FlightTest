__author__ = 'Akshai Rajendran'

from db_func import get_attr, get_allfid
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import DNS, smtplib, socket


#open config file and get username and api key
f = open('config.txt','r')
credentials = [line[line.index(':')+1:len(line)].strip() for line in f]

#credentials
mailbox = credentials[2]
pwd = credentials[3]

#this function gets all recipients for a given flight and date
def all_recip(date,ident):
    #give this function a date as an epoch and an ident it will give you all receipients for that flight
    #returns recipients in form [user,recipient]
    ids = get_allfid(date,ident)
    recips = [[get_attr('user',id),get_attr('recipient',id)] for id in ids]
    return recips

#this function sends a message to a list of [user,recipient] pairings
def dispatch(list,msg):
    for i in list:
        message = str(i[0]) + "'s flight " + msg
        #if it's an email address
        if '@' in i[1]:
            email(i[1], message)
        else:
            text(i[1], message)

#define the email and text functions
def email(recipient, message):
    #setup from and to addr
    from_addr = 'flight_serve@akshairajendran.com'
    to_addr = recipient

    #setup connection
    s = SMTP_SSL()
    s.connect('smtp.webfaction.com',465)
    s.login(mailbox,pwd)

    #setup message
    msg = 'Subject: %s\n\n%s' % ('Flight update from FlightServe', message)
    try:
        s.sendmail(from_addr,to_addr,msg)
    except:
        print "Didn't work"
    return

def text(recipient, message):
    #we just gonna text att, tmo, verizon and sprint...wutever
    att = recipient + '@txt.att.net'
    tmo = recipient + '@tmomail.net'
    vzw = recipient + '@vtext.com'
    sprint = recipient + '@messaging.sprintpcs.com'
    try:
        email(att, message)
        email(tmo, message)
        email(vzw, message)
        email(sprint, message)
    except:
        print "Didn't work"
    return

def main(data):
    #this function takes data from an incoming flight update and dispatches it accordingly
    #pull the departure date, ident, message from the data
    date = data['flight']['filed_departuretime']
    ident = data['flight']['ident']
    message = data['long_desc']
    #build the list of recipients
    recips = all_recip(date,ident)
    #dispatch the message
    dispatch(recips,message)
    #if it's an arrival, mark those flight id's as old (change the binary)

