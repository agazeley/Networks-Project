import socket
import time
import sys
from datetime import datetime


# Simple server class to handle GET and HEAD requests
class simple_server:
    def __init__ ( self , host , port , logging ):
        self.host = host
        self.port = port
        self.root_dir = 'www'
        self.log_file = 'log.txt'
        self._log = [ ]
        self.logging_on = logging

    def log ( self , message ):
        _time = datetime.now ( ).strftime ( '%Y-%m-%d %H:%M:%S' )
        if self.logging_on == True:
            self._log.append ( str ( _time ) + ": " + message )
        return

    def write_log ( self ):
        if self.logging_on == True:
            f = open ( self.log_file , 'a+' )
            for message in self._log:
                f.write ( message + '\r\n' )
            f.close ( )
        self._log = [ ]
        return

    def start_server ( self ):

        # Using out given host and port info we need to start the server up
        # Need to give the server a socket and bind the socket to the host:port
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )
        print ( "Spinning up the server on port " + str ( self.port ) )
        try:
            self.sock.bind ( (self.host , self.port) )

        except Exception as e:
            print ( "Server failed to startup...trying port 8080" )

            user_port = self.port
            self.port = 8080

            try:
                self.sock.bind ( (self.host , self.port) )
                print ( "Spinning up server on port " + str ( self.port ) )
            except Exception as e:
                print ( "Failed to bind sockets for ports " + str ( user_port ) + " and 8080. " )
                self.log ( "Failed to bind sockets for ports " + str ( user_port ) + " and 8080. " )
                self.shutdown ( )
                sys.exit ( 1 )
        print ( "Server running on " + self.host + ":" + str ( self.port ) )
        self.log ( "Server running on " + self.host + ":" + str ( self.port ) )
        self.accept_requests ( )
        self.write_log ( )

    def shutdown ( self ):
        # Used to quickly shutdown server
        try:
            self.sock.shutdown ( socket.SHUT_RDWR )
            print ( "Shutting down server....." )
            self.log ( "Shutting down server....." )
        except Exception as e:
            print ( "Why was there an exception thrown at shutdown?" )
            self.log ( "Why was there an exception thrown at shutdown?" )
        self.write_log ( )

    def accept_requests ( self ):

        while True:
            print ( "Waiting for connections" )
            # Change this number to change maximum number of requests
            self.sock.listen ( 2 )

            # Conn, addr is the connection object and the address of that connection for new connections
            conn , addr = self.sock.accept ( )
            reply = "Connection recieved from:" + str ( addr )
            print ( reply )
            self.log ( reply )
            data = conn.recv ( 1024 ).decode ( 'UTF-8' )

            # Figure out if the request method is GET or HEAD
            request_method = data.split ( ' ' )[ 0 ]
            print(request_method)


server = simple_server ( 'localhost' , 80 , True )
server.start_server ( )
