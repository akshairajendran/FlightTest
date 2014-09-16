__author__ = 'Akshai Rajendran'

from db_func import get_attr, get_allfid
from smtplib import SMTP
from email.mime.text import MIMEText

#open config file and get username and api key
f = open('config.txt','r')
credentials = [line[line.index(':')+1:len(line)].strip() for line in f]

#credentials
mailbox = credentials[2]
pwd = credentials[3]

#this function gets all recipients for a given flight and date
def all_recip(date,ident):
    #give this function a date as an epoch and an ident it will give you all receipients for that flight
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
    from_addr = 'flight_serve@akshairajendran.com'
    to_addr = recipient
    s = SMTP()
    print mailbox
    print pwd
    s.connect('smtp.webfaction.com')
    s.login(mailbox,pwd)
    s.sendmail(from_addr,to_addr,message)