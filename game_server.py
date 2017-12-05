import socket
import time
import json as js
import sys
import log
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

        while True:
            print ( "Waiting for connections" )
            # Change this number to change maximum number of requests
            self.sock.listen ( 4 )

            # Conn, addr is the connection object and the address of that connection for new connections
            conn , addr = self.sock.accept ( )
            thread._start_new_thread(self.new_client,(conn,addr))

            # Figure out if the request method is

    def handle(self,data):

        if data['req_type'] == 'new_game':
            # MAKE GAME ON SERVER
            players = (data['player'],'p2')
            self.games[self.id_int] = game(id=self.id_int,players=players)
            # return success message if successful
            request = self.make_server_request (self.id_int,'game_made',1 )
            self.id_int += 1

        elif data['req_type'] == 'join_game':
            game_id = data['req']
            self.games[game_id].players[1] = data['player']
            # return success message if successful
            request = self.make_server_request(game_id,'join_result',1)

        elif data['req_type'] == 'move':
            (x,y) = data['req']
            game_id = data[ 'game_id' ]
            result = self.games[data['game_id']].hit_or_miss(data['player'],x,y)
            if self.games[game_id].won_yet():
                print("Somebody won")
                request = self.make_server_request(game_id,'win',data['player'])
            else:
                request = self.make_server_request(game_id,'move_result',int(result))
                self.send_msg(request)
            # check victory comditions
        elif data['req_type'] == 'lobby_rdy':
            # make a lobby class to deal with lobby stuff?
            game_id = data[ 'game_id' ]
            if data['player'] == self.games[game_id].players[0]:
                self.games[game_id].ready[0] = True
                request = self.make_server_request(game_id,'player_rdy',0)
                self.send_msg(request)
            elif data['player'] == self.games[game_id].players[1]:
                self.games[ game_id ].ready[ 1 ] = True
                request = self.make_server_request(game_id,'player_rdy',1)
                self.send_msg(request)

            if self.games[ game_id ].ready == (True,True):
                request = self.make_server_request(game_id,'game_start',1)
                self.send_msg(request)
        elif data['req_type'] == 'board_setup':
        return

    def new_client(self,conn,addr):
        reply = "Connection recieved from:" + str ( addr )
        conn.send ( bytearray ( "Connection successful" , "utf-8" ) )

        data = conn.recv ( 1024 ).decode ( 'UTF-8' )
        data = js.loads(data)

        return

class game:

    def __init__(self,id=0,x_size=7,y_size=7,players=('p1','p2')):
        self.game_id = id
        self.x_size = x_size
        self.y_size = y_size
        self.players = players
        self.init_boards()
        self.move_log = [] # (player,x,y)
        self.num_hits = 0
        self.ships_sum = 100
        self.ready = (False,False)

    def init_boards(self,ships_sum,p1_board=None,p2_board=None):
        # tiles represented by tuples of (ship_bool,hit_bool)
        self.ships_sum = ships_sum
        self.p1_board = [[ (0,0) for x in range(self.x_size)] for y in range(self.y_size)]
        self.p2_board = [[ (0,0) for x in range(self.x_size)] for y in range(self.y_size)]
        self.update_boards(p1_board,p2_board)
        return
    def update_boards(self,p1_board=None,p2_board=None):
        if p1_board:
            for x in range(self.x_size):
                for y in range(self.y_size):
                    self.p1_board[x][y] = p1_board[x][y]
        if p2_board:
            for x in range(self.x_size):
                for y in range(self.y_size):
                    self.p2_board[x][y] = p2_board[x][y]
        return
    def hit_or_miss(self,player,x_pos,y_pos):
        hit = False
        if  player == self.players[0]:
            if self.p2_board[x_pos][y_pos][0]: # if ship bool true
                self.p2_board[ x_pos ][ y_pos ][1] = 1 # set hit bool to true
                self.num_hits += 1
                hit = True
            self.move_log.append((player,x_pos,y_pos))
        elif player == self.players[1]:
            if self.p1_board[x_pos][y_pos][0]: # if ship bool true
                self.p1_board[ x_pos ][ y_pos ][1] = 1 # set hit bool to true
                self.num_hits += 1
                hit = True
            self.move_log.append((player,x_pos,y_pos))
        else:
            print("Tried to make move with unknown player")
        return hit
    def won_yet(self):
        if self.num_hits == self.ships_sum:
            return 1
        else:
            return 0

server = game_server ( 'localhost' , 80 , True )
server.start_server ( )
