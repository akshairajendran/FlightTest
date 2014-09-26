__author__ = 'arajendran'

import cherrypy
from auth import AuthController, require, member_of, name_is
import db_func
import HTML
import flight_update

class Root:

    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    @cherrypy.expose
    def index(self):
        return """<html><body>
            <p>Welcome to FlightTest!</p>
            <a href="/auth/login">Login</a>
            <a href="/auth/register">Register</a>
        </body></html>"""

    @cherrypy.expose
    @require()
    def home(self,msg="You're now logged in."):
        return """<html><body>
            <p>Hello %s</p>
            %s</br></br>
            <a href="/new_flight">New Flight</a></br>
            <a href="/previous_flights">Previous Flights</a></br>
            <a href="/upcoming_flights">Upcoming Flights</a></br>
            <a href="/auth/logout">Logout</a></br>
        </html></body>""" %(cherrypy.request.login, msg)

    @cherrypy.expose
    @require()
    def new_flight(self, msg="Add new flight"):
        return """<html><body>
        <form method="post" action="/add_flight">
        %(msg)s<br />
        Departure Airport: <input type="text" name="airport_from"/><br />
        Arrival Airport: <input type="text" name="airport_to"/><br />
        Date: <input type="date" name="date"/><br />
        Carrier: <select name="carrier">
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
        Flight No.: <input type="number" name="flight_no"/><br />
        Recipient: <input type="text" name="recipient"/><br />
        <input type="submit" value="Add Flight" /></br>
        <a href="/home">Home</a>
        </form></html></body>""" % locals()

    @cherrypy.expose
    @require()
    def add_flight(self, airport_from=None, airport_to=None, date=None, carrier=None, flight_no=None, recipient=None):
        if len(airport_from) < 1 or len(airport_to) < 1 or date=='' or len(carrier) < 1 or len(flight_no) < 1 or len(recipient) < 1:
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
            db_func.add_flight(cherrypy.request.login,airport_from,airport_to,date,carrier,flight_no, recipient)
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
            flight_update.del_alert(db_func.get_attr('date',flightid),db_func.get_attr('carrier',flightid),db_func.get_attr('flight_no',flightid), db_func.get_attr('airport_from',flightid))
        db_func.del_flight(cherrypy.request.login, int(flightid))
        raise cherrypy.HTTPRedirect("/upcoming_flights")


if __name__ == '__main__':
    cherrypy.quickstart(Root())