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
            self.sock.listen ( 10 )

            # Conn, addr is the connection object and the address of that connection for new connections
            conn , addr = self.sock.accept ( )
            reply = "Connection recieved from:" + str ( addr )
            print ( reply )
            self.log ( reply )
            data = conn.recv ( 1024 ).decode ( 'UTF-8' )

            # Figure out if the request method is GET or HEAD
            request_method = data.split ( ' ' )[ 0 ]

            print ( "Request method: " + request_method )
            print ( "Request message: " + data )
            self.log ( "Request method: " + request_method + '\n' + "Request message: \n" + data )

            if request_method.upper ( ) == 'GET' or request_method.upper ( ) == 'HEAD':

                file_requested = data.split ( ' ' )

                # get second element
                file_requested = file_requested[ 1 ]
                # Check for URL arguments. Disregard them
                file_requested = file_requested.split ( '?' )[ 0 ]

                if file_requested == '/':
                    file_requested = '/index.html'

                file_requested = self.root_dir + file_requested
                print ( "Requested file: " + file_requested )
                self.log ( "Requested file: " + file_requested )

                # load file
                try:
                    file_handler = open ( file_requested , 'rb' )
                    if request_method.upper ( ) == 'GET':
                        # Only get the file when method is GET
                        response_content = file_handler.read ( )

                    file_handler.close ( )
                    response_headers = self.create_http_header ( 200 )
                # if the file isnt found in the default dir generate 404 page
                except Exception as E:
                    print ( "File not found. 404 response sent" )
                    self.log ( "File not found. 404 response sent" )
                    response_headers = self.create_http_header ( 404 )

                    if request_method == 'GET':
                        response_content = b"<html><body><p>Error 404: File not found</p><p>Andrew's Python HTTP server</p></body></html>"
                # create headers for GET or HEAD
                server_response = response_headers.encode ( )
                if request_method == 'GET':
                    server_response += response_content

                conn.send ( server_response )
                self.log ( server_response )
                self.log ( "Message sent. Closing connection." )
                print ( "Closing connection" )
                self.write_log ( )
                conn.close ( )
            elif request_method.upper ( ) == 'POST':

                print ( "Post method detected" )
                data = data.split ( )

                referer = ""
                i = 0
                while str ( data[ i ] ) != 'Referer:':
                    if str ( data[ i ] ) == 'Referer:': referer = str ( data[ i + 1 ] )
                    i += 1
                # print("Referer: " + referer)
                message = data[ -1 ].split ( "&" )
                dict = {}
                for entry in message:
                    entry = entry.split ( '=' )
                    dict[ str ( entry[ 0 ] ) ] = str ( entry[ 1 ] )

                response_headers = self.create_http_header ( 303 )

                if len ( dict.items ( ) ) > 0:
                    response_content = "<html><body>"
                    for item , content in dict.items ( ):
                        response_content += "<p>"
                        response_content += item
                        response_content += ": "
                        response_content += content
                        response_content += "</p>"

                    response_content += "<p>Andrew's Python HTTP server</p></body></html>"
                else:
                    response_content = b"<html><body><p>Error no POST data sent</p><p>Andrew's Python HTTP server</p></body></html>"

                server_response = response_headers.encode ( )
                server_response += response_content.encode ( )

                conn.send ( server_response )

                print ( "Closing connection" )
                self.log ( "Message sent. Closing connection." )
                self.write_log ( )
            else:
                print ( "Unknown request method: " + request_method )
                self.log ( "Unknown request method: " + request_method )
                self.write_log ( )


server = simple_server ( 'localhost' , 80 , True )
server.start_server ( )
