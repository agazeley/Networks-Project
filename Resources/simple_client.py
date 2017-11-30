import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# server_address = ('10.200.100.21', 50001)
server_address = ('localhost', 50001)

print('connecting to %s port %s' % server_address)
sock.connect(server_address)



while True:
    msg = input("Send a message: ")
    size = len(msg)
    msg = msg.encode()
    sock.sendall(msg)
    reply = sock.recv(size).decode('UTF-8')
    if reply:
        print("Received: " + str(reply))
