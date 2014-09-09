__author__ = 'arajendran'

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler


server = SimpleJSONRPCServer(('localhost', 13167), requestHandler=SimpleJSONRPCRequestHandler, logRequests=True)

server.register_function(pow)
server.register_function(lambda x,y: x+y, 'add')
server.register_function(lambda x: x, 'ping')
server.register_function(lambda x,y: x*y, 'mult')
server.serve_forever()
