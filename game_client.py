import socket
import sys
import time
import log


class client:
    def __init__ ( self , host , port ):
        self.server_ip = host
        self.server_port = port
        self.logger = log.logger('game')
        self.msg_size = 2048

    def start_client ( self ):
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )
        print ( 'connecting to %s port ' + str(self.server_port) )
        try:
            sock.connect ( (self.server_ip , self.server_port) )

        except Exception as e:
            print ( "Failed to connect to server" )
            self.logger.log ( str ( e ) )
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




# Create a TCP/IP socket
sock = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )

# Connect the socket to the port where the server is listening
# server_address = ('10.200.100.21', 50001)
server_address = ('localhost' , 50001)

usr_client = client('localhost',50001)
usr_client.start_client()
usr_client.run()

