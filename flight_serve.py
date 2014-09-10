__author__ = 'arajendran'

import SocketServer
import json

# from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
# from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler
# from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher
#
# server = SimpleJSONRPCServer(('localhost', 13167), requestHandler=SimpleJSONRPCRequestHandler, logRequests=True)
#
# server.register_function(pow)
# server.register_function(lambda x,y: x+y, 'add')
# server.register_function(lambda x: x, 'ping')
# server.register_function(lambda x,y: x*y, 'mult')
# server.serve_forever()

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            #take the data and print it
            data = self.request.recv(1024).strip()
            print data
            # send some 'ok' back
            self.request.sendall(json.dumps({"Content-type":"text/plain", 'result':'ok'}))
        except Exception, e:
            print "Exception while receiving message: ", e

server = MyTCPServer(('127.0.0.1', 13167), MyTCPServerHandler)
server.serve_forever()