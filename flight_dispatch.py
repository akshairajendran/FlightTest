__author__ = 'Akshai Rajendran'

from db_func import get_attr, get_allfid, mark_old
from flight_update import del_alert
from smtplib import SMTP_SSL
import datetime


#open config file and get username and api key
f = open('config.txt','r')
credentials = [line[line.index(':')+1:len(line)].strip() for line in f]

#credentials
mailbox = credentials[2]
pwd = credentials[3]

#this function gets all recipients for a given flight and date
def all_recip(date,ident,airport_from):
    #give this function a date as an epoch and an ident it will give you all receipients for that flight
    #returns recipients in form [user,recipient]
    ids = get_allfid(date,ident,airport_from)
    recips = [[get_attr('user',id),get_attr('recipient',id)] for id in ids]
    return recips

#this function sends a message to a list of [user,[recipient1,recipient2,...]] pairings
def dispatch(list,msg):
    for i in list:
        message = str(i[0]) + "'s flight " + msg
        for recip in i[1]:
            #if it's an email address
            if '@' in recip:
                email(recip, message)
            else:
                text(recip, message)

#define the email and text functions
def email(recipient, message):
    #setup from and to addr
    from_addr = 'update@flyteshare.com'
    to_addr = recipient

    #setup connection
    s = SMTP_SSL()
    s.connect('smtp.webfaction.com',465)
    s.login(mailbox,pwd)

    #setup message
    msg = 'Subject: %s\n\n%s' % ('Flight update from FlyteShare', message)
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
    date_format = datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
    ident = data['flight']['ident']
    airport_from = data['flight']['origin'][1:]
    event = data['eventcode']
    message = data['long_desc']
    #build the list of recipients
    recips = all_recip(date,ident,airport_from)
    #dispatch the message
    dispatch(recips,message)
    #once it's departed we'll mark it old
    if event == 'departure':
        ids = get_allfid(date,ident,airport_from)
        mark_old(ids)
    else:
        pass
    #if it's an arrival, mark those flight id's as old (change the binary)
    #we do this a second time in case it didn't work the first time
    #also delete the alert because we're now done tracking it
    if event == 'arrival' or event == 'cancelled':
        ids = get_allfid(date,ident,airport_from)
        mark_old(ids)
        del_alert(date=date_format,airport_from=airport_from,identifier=ident)
    else:
        pass



