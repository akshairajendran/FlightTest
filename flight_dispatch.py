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

def checkmail(mail):
        DNS.DiscoverNameServers()
        print "checking %s..."%(mail)
        hostname = mail[mail.find('@')+1:]
        mx_hosts = DNS.mxlookup(hostname)
        failed_mx = True
        for mx in mx_hosts:
                smtp = smtplib.SMTP()
                try:
                        smtp.connect(mx[1])
                        print "Stage 1 (MX lookup & connect) successful."
                        failed_mx = False
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((mx[1], 25))
                        s.recv(1024)
                        s.send("HELO %s\n"%(mx[1]))
                        s.recv(1024)
                        s.send("MAIL FROM:< test@test.com>\n")
                        s.recv(1024)
                        s.send("RCPT TO:<%s>\n"%(mail))
                        result = s.recv(1024)
                        print result
                        if result.find('Recipient address rejected') > 0:
                                print "Failed at stage 2 (recipient does not exist)"
                        else:
                                print "Adress valid."
                                failed_mx = False
                        s.send("QUIT\n")
                        break
                except smtplib.SMTPConnectError:
                        continue
        if failed_mx:
                print "Failed at stage 1 (MX lookup & connect)."
        print ""
        if not failed_mx:
                return True
        return False
