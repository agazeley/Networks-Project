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
        self.clients = {} # (ip,port,name,game_id)

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


            if data:
                data = data.decode()
                data = js.loads(data)
                print ( data )
                if data[ 'req_type' ] == 'connect':
                    print ( "New connection recieved from: " + str ( (ip , port) ) )
                    self.clients[ conn_int ] = (ip , port , data[ 'player' ] , None)
                    self.sock.sendto ( bytearray ( self.make_server_request ( 0 , 'conn_request' , 1 ) , "utf-8" ) ,
                                       (ip , port) )
                    conn_int += 1
                else:
                    request = self.handle(data)

                    if request:
                        if type(request) == type([]):
                            for item in request:
                                self.sock.sendto ( bytearray (item[0] , 'utf-8' ), (item[1] ,item[2]))
                        else:
                            self.sock.sendto(bytearray(str(request),'utf-8'),(ip,port))
        return

    # Figure out if the request method is

    def handle(self,data):
        print("Recieved: " + str(data))
        if data['req_type'] == 'new_game':
            # MAKE GAME ON SERVER
            players = (data['player'],'p2')
            new_game = game(id=self.id_int,players=players)
            self.games[self.id_int] = new_game
            # return success message if successful
            request = self.make_server_request (self.id_int,'game_made',1 )
            self.id_int += 1
            print("Game made: "+ str(new_game.players))
            return request
        elif data['req_type'] == 'join_game':
            game_id = data['req']
            if self.games[game_id]:
                self.games[game_id].players = (self.games[game_id].players[0],data['player'])
                # return success message if successful
                request = self.make_server_request(game_id,'join_result',1)
                for i in range(len(self.clients)):
                    if data['player'] == self.clients[i][2]:
                        # (ip,port,name,game_id)
                        (ip,port,name,_old_game_id) = self.clients[i]
                        self.clients[i] = (ip,port,name,game_id)
                print(self.clients)
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
                # Need to send message to both players that the game is starting
                request = [ ]
                for client in self.clients.items():
                    if client[1][3] == game_id:
                        c = []
                        c.append(self.make_server_request ( game_id , 'game_start' , 1 ))
                        c.append(client[1][0])
                        c.append(client[1][1])
                        request.append(c)
                print("Both players ready in game: " ,str(game_id))
                # Resets for board setup
                self.games[ game_id ].ready = (False,False)
                print(request)
                return request
            elif self.games[game_id].ready == (True,False):
                request = self.make_server_request(game_id,'player',(True,False))
            elif self.games[game_id].ready == (False,True):
                request = self.make_server_request ( game_id , 'player' , (False , True) )
            print("Players ready: " + str(self.games[game_id].ready))
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


    # OUTDATED AND UNUSED
    def new_client(self,ip,port,id):

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

class game:

    def __init__(self,id=0,x_size=7,y_size=7,players=('p1','p2')):
        self.game_id = id
        self.x_size = x_size
        self.y_size = y_size
        self.players = players
        self.init_boards(100)
        self.move_log = [] # (player,x,y,result)
        self.num_hits = 0
        self.ready = (False,False)
        self.turn = True # True = p1, false = p2
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
        elif p2_board:
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
            self.move_log.append((player,x_pos,y_pos,hit))
        elif player == self.players[1]:
            if self.p1_board[x_pos][y_pos][0]: # if ship bool true
                self.p1_board[ x_pos ][ y_pos ][1] = 1 # set hit bool to true
                self.num_hits += 1
                hit = True
            self.move_log.append((player,x_pos,y_pos,hit))
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
