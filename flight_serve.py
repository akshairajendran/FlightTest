__author__ = 'arajendran'

import SocketServer
import json
import flight_dispatch

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            #take the data and print it
            data = self.request.recv(9192).strip()
            # send some 'ok' back
            self.request.sendall("HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + "2" + "\r\n\r\n" + "ok")
            data = json.loads(data[data.index('{'):])
            flight_dispatch.main(data)
        except Exception, e:
            print "Exception while receiving message: ", e


server = MyTCPServer(('127.0.0.1', 13167), MyTCPServerHandler)
server.serve_forever()