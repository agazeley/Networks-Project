import socket
import sys
import os

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
    data = data.lower ( ).strip ( '!' )

    reply = data
    send_msg ( connection , reply )

    # Handles hello message
    '''
    if data == "hello server":
        reply = 'Hello client'
        send_msg ( connection , reply )

    # handles file request
    elif data == "give me the file":
        size = file_size ( file )
        send_msg ( connection , str ( size ) )

    # handles client ready message
    elif data == "i am ready":
        with open ( file , 'r' ) as myfile:
            reply = myfile.read ( )
            send_msg ( connection , reply )

    # Handles thank you message
    elif data == "thank you":
        reply = "Goodbye"
        send_msg ( connection , reply )

    # Catch all
    else:
        _reply = 'Do not understand server command'
        send_msg ( connection , _reply )
    '''


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
	
    try:
        run = True

        print ('connection from ' + str(client_address))
        # Receive the data in small chunks and retransmit it
        while run:
            data = connection.recv(1024).decode('UTF-8')
            print ('received: ' + str(data))
            # If a message is recieved handle the message
            if data:
                data = data.split()
                handle(connection,data)
            else:
                print('no more data from ' +str(client_address))
                break
            
    finally:
        # Clean up the connection
        connection.close()
