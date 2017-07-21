import socket
from datetime import datetime

server_address = ('localhost', 6789)
max_size = 4096

print('Starting the server at %s' % datetime.now())
print('Waiting for client to call.')
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)

data, client = server.recvfrom(max_size)

print('At %s %s said %s' % (datetime.now(), client, data))
server.sendto(b'Are you talking to me?', client)
server.close()
