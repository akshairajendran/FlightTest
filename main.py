__author__ = 'arajendran'

import cherrypy
from auth import AuthController, require, member_of, name_is

class RestrictedArea:

    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group

    _cp_config = {
        'auth.require': []
    }

    @cherrypy.expose
    def index(self):
        return """This is the admin only area."""


class Root:

    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    restricted = RestrictedArea()

    @cherrypy.expose
    def index(self):
        return """<html><body>
            <p>Welcome to FlightTest!</p>
            <a href="/auth/login">Login</a>
        </body></html>"""

    @cherrypy.expose
    @require()
    def home(self):
        return """<html><body>
            <p>Hello %s, you're now logged in.</p>
            <a href="/auth/logout">Logout</a>
        </html></body>""" %cherrypy.request.login

    @cherrypy.expose
    @require(name_is("joe"))
    def only_for_joe(self):
        return """Hello Joe - this page is available to you only"""

    # This is only available if the user name is joe _and_ he's in group admin
    @cherrypy.expose
    @require(name_is("joe"))
    @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
    def only_for_joe_admin(self):
        return """Hello Joe Admin - this page is available to you only"""


if __name__ == '__main__':
    cherrypy.quickstart(Root())