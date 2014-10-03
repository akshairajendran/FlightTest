__author__ = 'arajendran'

import cherrypy
from auth import AuthController, require, member_of, name_is
import db_func
import HTML
import flight_update
import os

class Root:

    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    @cherrypy.expose
    def index(self):
        return """<html>
        <head>
        <link rel="stylesheet" type="text/css" href="static/css/index.css"/>
        </head>
        <body>
            <div class='main'>
                <p>Welcome to FlightTest!</p>
                <a href="/auth/login">Login</a>
                <a href="/auth/register">Register</a>
            </div>
        </body></html>"""

    @cherrypy.expose
    @require()
    def home(self,msg="You're now logged in."):
        return """<html>
        <head>
        <link rel="stylesheet" type="text/css" href="static/css/home.css"/>
        </head>
        <body>
            <div class='main'>
                <p>Hello %s</p>
                <p1>%s</br></br></p1>
                <a href="/new_flight">New Flight</a></br>
                <a href="/previous_flights">Previous Flights</a></br>
                <a href="/upcoming_flights">Upcoming Flights</a></br>
                <a href="/auth/logout">Logout</a></br>
            </div>
        </html></body>""" %(cherrypy.request.login, msg)

    @cherrypy.expose
    @require()
    def new_flight(self, msg="Add new flight"):
        return """<html>
        <head>
        <link rel="stylesheet" type="text/css" href="static/css/newflight.css"/>
        </head>
        <body>
        <div class='main'>
            <form method="post" action="/add_flight">
            <p>%(msg)s<br /></p>
            <div class='inputs'>
                <label>Departure Airport: </label><input type="text" name="airport_from"/><br />
                <label>Arrival Airport: </label><input type="text" name="airport_to"/><br />
                <label>Date: </label><input type="date" name="date"/><br />
                <label>Carrier: </label><select name="carrier">
                <option value="AirTran">AirTran</option>
                <option value="Alaska">Alaska</option>
                <option value="American">American</option>
                <option value="Delta">Delta</option>
                <option value="Frontier">Frontier</option>
                <option value="Hawaiian">Hawaiian</option>
                <option value="JetBlue">JetBlue</option>
                <option value="Southwest">Southwest</option>
                <option value="Spirit">Spirit</option>
                <option value="United">United</option>
                <option value="US Airways">US Airways</option>
                <option value="Virgin">Virgin</option>
                </select><br />
                <label>Flight No.: </label><input type="number" name="flight_no"/><br />
                <label>Recipient: </label><input type="text" name="recipient1"/><br />
                <label>Recipient: </label><input type="text" name="recipient2"/><br />
                <label>Recipient: </label><input type="text" name="recipient3"/><br />
                <label>Recipient: </label><input type="text" name="recipient4"/><br />
                <label>Recipient: </label><input type="text" name="recipient5"/><br />
            </div>
            <div class='bottom'>
                <input type="submit" value="Add Flight" /></br>
                <a href="/home">Home</a>
            </div>
        </div>
        </form></html></body>""" % locals()

    @cherrypy.expose
    @require()
    def add_flight(self, airport_from=None, airport_to=None, date=None, carrier=None, flight_no=None, recipient1=None, recipient2=None, recipient3=None,recipient4=None,recipient5=None):
        if len(airport_from) < 1 or len(airport_to) < 1 or date=='' or len(carrier) < 1 or len(flight_no) < 1 or len(recipient1) < 1:
            return self.new_flight("Please enter all information")
        else:
            if db_func.check_myflight(user=cherrypy.request.login,date=date, carrier=carrier, flight_no=flight_no):
                return self.new_flight("You've already entered this flight")
            else:
                pass
            if db_func.check_flight(user=cherrypy.request.login,date=date, carrier=carrier, flight_no=flight_no):
                pass
            else:
                if flight_update.check_flight(airport_from,airport_to,date,carrier,flight_no):
                    flight_update.set_alert(airport_from,airport_to,date,carrier,flight_no)
                else:
                    return self.new_flight("Please enter a valid flight")
            all_recipients = [recipient1,recipient2,recipient3,recipient4,recipient5]
            recipients = [recip for recip in all_recipients if len(recip)>=5]
            db_func.add_flight(cherrypy.request.login,airport_from,airport_to,date,carrier,flight_no, recipients)
            return self.home(msg="Your flight has been added.")

    @cherrypy.expose
    @require()
    def previous_flights(self):
        list = db_func.display_flights(cherrypy.request.login,1)
        htmlcode = HTML.table(list, ['Departure Airport','Arrival Airport','Date','Carrier','Flight No.'])
        return """<html><body>
        %s </br>
        <a href="/home">Home</a>
        </body></html>""" % htmlcode

    @cherrypy.expose
    @require()
    def upcoming_flights(self):
        list = db_func.display_flights(cherrypy.request.login,0)
        htmlcode = HTML.table(list, ['Departure Airport','Arrival Airport','Date','Carrier','Flight No.'])
        return """<html><body>
        %s </br>
        <a href="/home">Home</a>
        </body></html>""" % htmlcode

    @cherrypy.expose
    @require()
    def rec_flight(self,flightid):
        list = db_func.display_recipients(cherrypy.request.login,flightid)
        htmlcode = HTML.table(list, ['Recipients'])
        return """<html><body>
        %s </br>
        <a href="/home">Home</a>
        </body></html>""" % htmlcode

    @cherrypy.expose
    @require()
    def del_flight(self,flightid):
        if db_func.check_flight(user=cherrypy.request.login,flightid=flightid):
            pass
        else:
            flight_update.del_alert(date=db_func.get_attr('date',flightid),carrier=db_func.get_attr('carrier',flightid),flight_no=db_func.get_attr('flight_no',flightid), airport_from=db_func.get_attr('airport_from',flightid))
        db_func.del_flight(cherrypy.request.login, int(flightid))
        raise cherrypy.HTTPRedirect("/upcoming_flights")

cherrypy.config.update({
    'server.socket_port':22428
})

if __name__ == '__main__':
    conf = {
     '/': {
         'tools.sessions.on': True,
         'tools.staticdir.root': os.path.abspath(os.getcwd())
     },
     '/static': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './pub/'
     }
    }
    cherrypy.quickstart(Root(),'/',conf)