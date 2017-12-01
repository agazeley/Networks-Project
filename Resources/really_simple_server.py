import socket
import sys
import os
import socket

# https://stackoverflow.com/questions/36083964/i-got-a-connection-error-in-my-socket-program
HOST="localhost"
PORT=50001

mySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind( (HOST, PORT) )
mySocket.listen(1)
print("Waiting for connection")

connection, address=mySocket.accept()
print("Connection recieved from:", address[0])

connection.send(bytearray("Connection successful", "utf-8"))
clientMessage=connection.recv(1024)

while clientMessage != "Client: end":
    if not clientMessage:
        break
    clientMessage = clientMessage.decode()
    print (clientMessage)
    connection.send(bytearray(clientMessage, "utf-8"))
    clientMessage=connection.recv(1024)

print("Connection ended.")
connection.close()

''''Trying something new
# get total bits in a filesize
# used to transfer longer than 1024 bit messages
def file_size(filename):
    utf8_text = open(filename,'r+').read()
    unicode_data = utf8_text
    return len(unicode_data)

# function to quickly send a message over a connection and print the message
def send_msg(connection,msg):
    print("sending: " + msg)
    msg = msg.encode()
    connection.sendall(msg)
    return
# default request handler
def handle(connection,data):
    file = "server_data_test.txt"
    data = data.lower().strip('!')
    reply = input("Enter reply: ")
    send_msg(connection,reply)
    return

#Sever setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('10.200.100.8',50001)
server_address = ('localhost',50001)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1) 

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    connection.send(bytearray("Connection successful",'utf-8'))
    try:
        run = True

        print ('connection from ' + str(client_address))
        # Receive the data in small chunks and retransmit it
        while run:
            data = connection.recv(1024).decode('UTF-8')
            print ('received: ' + str(data))
            # If a message is recieved handle the message
            if data:
                handle(connection,data)
            else:
                print('no more data from ' +str(client_address))
                break
    finally:
        # Clean up the connection
        connection.close()
        print("Connection closed")
'''