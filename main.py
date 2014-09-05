__author__ = 'arajendran'

import cherrypy
from auth import AuthController, require, member_of, name_is
import db_func

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
            <a href="/auth/logout">Logout</a>
        </html></body>""" %(cherrypy.request.login, msg)

    @cherrypy.expose
    @require()
    def new_flight(self, msg="Add new flight"):
        return """<html><body>
        <form method="post" action="/add_flight">
        %(msg)s<br />
        Departure Airport: <input type="text" name="airport_from"/><br />
        Arrival Airport: <input type="text" name="airport_to"/><br />
        Date: <input type="date" name="date" value=""/><br />
        Carrier: <input type="text" name="carrier"/><br />
        Flight No.: <input type="number" name="flight_no"/><br />
        <input type="submit" value="Add Flight" />
        </html></body>""" % locals()

    @cherrypy.expose
    @require()
    def add_flight(self, airport_from=None, airport_to=None, date=None, carrier=None, flight_no=None):
        if airport_from is None or airport_to is None or date == "" or carrier is None or flight_no is None:
            return self.new_flight("Please enter all information")
        else:
            db_func.add_flight(cherrypy.request.login,airport_from,airport_to,date,carrier,flight_no)
            return self.home(msg="Your flight has been added.")




if __name__ == '__main__':
    cherrypy.quickstart(Root())