import socket
from datetime import datetime

server_address = ('localhost', 6789)
max_size = 4096

print('Starting the client at %s' % datetime.now())
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'Hey!', server_address)
data, server = client.recvfrom(max_size)
print('At %s %s said %s' % (datetime.now(), server, data))
client.close()
