__author__ = 'arajendran'

import SocketServer
import json
import db_func

#define functions to clean and handle data
def formatter(data):
    #returns long_desc and ident
    index = data.index('{')
    data = str(data[index:] + '}}')
    longdesc_index = data.index('long_desc')
    shortdesc_index = data.index('short_desc')
    ident_index = data.index('ident')
    aircraft_index = data.index('aircrafttype')
    long_desc = data[longdesc_index:shortdesc_index-3].translate(None,'"')
    ident = data[ident_index:aircraft_index-3].translate(None,'"')
    long_desc = long_desc[long_desc.index(':')+1:]
    ident = ident[ident.index(':')+1:]
    return [long_desc, ident]

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            #take the data and print it
            data = self.request.recv(1024).strip()
            results = formatter(data)
            print results[0]
            print results[1]
            # send some 'ok' back
            self.request.sendall("""HTTP/1.0 200 OK\r Content-Type: text/plain;""")
        except Exception, e:
            print "Exception while receiving message: ", e

server = MyTCPServer(('127.0.0.1', 13167), MyTCPServerHandler)
server.serve_forever()