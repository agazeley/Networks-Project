import socket
import sys
import time
import log


class client:
    def __init__ ( self , host , port ):
        self.server_ip = host
        self.server_port = port
        self.logger = log.logger('client')
        self.msg_size = 2048

    def start_client ( self ):
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )
        print ( 'connecting to %s port ' + str(self.server_port) )
        try:
            sock.connect ( (self.server_ip , self.server_port) )
        except Exception as e:
            print ( "Failed to connect to server" )
            self.logger.log ( str ( e ) )
            self.logger.write_log()
        return

    def run(self):
        while True:
            msg = input ( "Send a message: " )
            size = len ( msg )
            msg = msg.encode ( )
            sock.sendall ( msg )
            reply = sock.recv ( self.msg_size ).decode ( 'UTF-8' )
            if reply:
                print ( "Received: " + str ( reply ) )
        return

    def send_msg(self,msg):
        msg = str ( msg )
        print ( "sending: " + msg )
        msg = msg.encode ( )
        self.sock.sendall ( msg )
        return

class game:

    def __init__(self,ip,port):
        self.client_port = port
        self.client_ip = ip
        self.client = client(self.client_ip,self.client_port)
        self.logger = log.logger("game")

        return

    def start(self):
        self.client.start_client()
        self.name = input("What is your name?")

    def menu(self):
        print ( "1. Play" )
        print ( "2. Connect" )
        inp = True
        while inp:
            selection = self.get_menu_input()
            if selection == 1 or selection == 2:
                #inp = False
                if selection == 1:
                    self.client.send_msg(selection)
                    reply = sock.recv ( self.msg_size ).decode ( 'UTF-8' )
                    print(reply)
                    # Do something in the client
                elif selection == 2:
                    self.client.send_msg ( selection )
                    reply = sock.recv ( self.msg_size ).decode ( 'UTF-8' )
                    print(reply)
                    # Do something else in the client

    def get_menu_input(self):
        cmd = input("What do you want to do? ")
        try:
            cmd = int(cmd)
        except Exception as e:
            print("Failed to conver to int. Try again.")
            self.logger.log(str(e))
            self.logger.write_log()

        return cmd




# Create a TCP/IP socket
sock = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )

# Connect the socket to the port where the server is listening
# server_address = ('10.200.100.21', 50001)
server_address = ('localhost' , 50001)

usr_client = game('localhost',50001)
usr_client.start()
usr_client.menu()

