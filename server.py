import socket
import sys

from threading import Thread, Semaphore

# Connect with server through UDP socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    print(data)


