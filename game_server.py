import socket
import time
import json as js
import sys
import log
from server_game import game
import threading as thread
from datetime import datetime


# Simple server class to handle GET and HEAD requests
class game_server:
    def __init__ ( self , host , port , logging ):
        self.host = host
        self.port = port
        self.root_dir = 'www'
        self.logger = log.logger ( 'server' )
        self.games = {} # key = game_id, item = game object
        self.id_int = 0
        self.clients = {} # (conn,addr,name,game_id)

    def make_server_request(self,game_id,type,msg):
        data = {}
        data['game_id'] =game_id
        data['type'] = type
        data['msg'] = msg
        data = js.dumps(data)
        return data

    def start_server ( self ):

        # Using out given host and port info we need to start the server up
        # Need to give the server a socket and bind the socket to the host:port
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_DGRAM )
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
                self.logger.log ( "Failed to bind sockets for ports " + str ( user_port ) + " and 8080. " )
                self.shutdown ( )
                sys.exit ( 1 )
        print ( "Server running on " + self.host + ":" + str ( self.port ) )
        self.logger.log ( "Server running on " + self.host + ":" + str ( self.port ) )
        self.accept_requests ( )
        self.logger.write_log ( )

    def shutdown ( self ):
        # Used to quickly shutdown server
        try:
            self.sock.shutdown ( socket.SHUT_RDWR )
            print ( "Shutting down server....." )
            self.logger.log ( "Shutting down server....." )
        except Exception as e:
            print ( "Why was there an exception thrown at shutdown?" )
            self.logger.log ( "Why was there an exception thrown at shutdown?" )
        self.logger.write_log ( )

    def send_msg(self,msg):
        msg = str(msg)
        msg = msg.encode()
        self.sock.sendall(msg)
        print("Sent" + str(msg))
        return

    def accept_requests ( self ):
        print("Waiting for connections")
        conn_int = 0
        while True:

            # Change this number to change maximum number of requests
            # Conn, addr is the connection object and the address of that connection for new connections
            data , (ip,port) = self.sock.recvfrom(1024)
            if data.decode().lower() == 'hi server':
                print ( "New connection recieved" )
                self.clients[conn_int] = (ip,port,"",None)
                thread._start_new_thread(self.new_client,(ip,port,conn_int))
                conn_int += 1
            # Figure out if the request method is

    def handle(self,data):
        print(data)
        if data['req_type'] == 'new_game':
            # MAKE GAME ON SERVER
            players = (data['player'],'p2')
            new_game = game(id=self.id_int,players=players)
            self.games[self.id_int] = new_game
            # return success message if successful
            request = self.make_server_request (self.id_int,'game_made',1 )
            self.id_int += 1
            print(str(new_game.players))
            return request
        elif data['req_type'] == 'join_game':
            game_id = data['req']
            if self.games[game_id]:
                self.games[game_id].players = (self.games[game_id].players[0],data['player'])
                # return success message if successful
                request = self.make_server_request(game_id,'join_result',1)
                return request
            else:
                request = self.make_server_request(game_id,'join_result',0)
                return request
        elif data['req_type'] == 'move':
            (x,y) = data['req']
            game_id = data[ 'game_id' ]
            #Check to make sure its you turn/board placement is complete
            if self.games[game_id].ready == (False,True) or self.games[game_id].ready == (True,False) or self.games[game_id].ready == (False,False):
                request = self.make_server_request(game_id,"move_result","not yet")
                return request
            result = self.games[game_id].hit_or_miss(data['player'],x,y)
            if self.games[game_id].won_yet():
                print("Somebody won")
                request = self.make_server_request(game_id,'win',data['player'])
                return request
            else:
                request = self.make_server_request(game_id,'move_result',int(result))
                return request
        elif data['req_type'] == 'lobby_rdy':
            # make a lobby class to deal with lobby stuff?
            game_id = data[ 'game_id' ]
            # Logic behind ready up
            if data['player'] == self.games[game_id].players[0] and self.games[game_id].ready[1] == False:
                (p1,p2) = self.games[game_id].ready
                self.games[ game_id ].ready = (True,False)
            elif data['player'] == self.games[game_id].players[1] and self.games[game_id].ready[0] == False:
                (p1,p2) = self.games[game_id].ready
                self.games[ game_id ].ready = (False,True)
            elif data[ 'player' ] == self.games[ game_id ].players[ 0 ] and self.games[ game_id ].ready[ 1 ] == True:
                (p1 , p2) = self.games[ game_id ].ready
                self.games[ game_id ].ready = (True , True)
            elif data[ 'player' ] == self.games[ game_id ].players[ 1 ] and self.games[ game_id ].ready[ 0 ] == True:
                (p1 , p2) = self.games[ game_id ].ready
                self.games[ game_id ].ready = (True , True)

            #Logic behind ready requests
            if self.games[ game_id ].ready == (True,True):
                request = self.make_server_request(game_id,'game_start',1)
                # Resets for board setup
                self.games[ game_id ].ready = (False,False)
            elif self.games[game_id].ready == (True,False):
                request = self.make_server_request(game_id,'player',(True,False))
            elif self.games[game_id].ready == (False,True):
                request = self.make_server_request ( game_id , 'player' , (False , True) )
            return request
        elif data['req_type'] == 'board_setup':
            game_id = data['game_id']
            # make the gameboard using the board sent in data
            new_board = data['req']
            if data['player'] == self.games[game_id].players[0]:
                self.games[game_id].update_boards(p1_board = new_board)
            else:
                self.games[game_id].update_boards(p2_board = new_board)
        return

    def new_client(self,ip,port,id):
        reply = "Connection recieved from:" + str ( ip ) + ":" + str(port)
        self.sock.sendto ( bytearray ( "Connection successful" , "utf-8" ),(ip,port) )
        data = js.loads(self.sock.recv ( 1024 ).decode ( 'UTF-8' ))
        (ip,port,player,game_id) = self.clients[id]
        self.clients[id] = (ip,port,data['player'],game_id)
        while True:
            data = self.sock.recv ( 1024 ).decode ( 'UTF-8' )
            if data:
                data = js.loads(data)
            # what do we do when a new client connects?
            request = self.handle(data)
            if request:
                print("Sending: " + request)
                self.sock.sendto(bytearray(request,'utf-8'),(ip,port))
        return


server = game_server ( 'localhost' , 80 , True )
server.start_server ( )
