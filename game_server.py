import socket
import time
import json as js
import sys
import log
import threading as thread
from datetime import datetime

class player:
    def __init__(self,name,ip,port,board=None):
        self.name = name
        self.ready = False
        self.ip = ip
        self.port = port
        self.board = board
        return

class game:

        def __init__ ( self , id=0 , x_size=7 , y_size=7 , players=('p1' , 'p2') ):
            self.game_id = id
            self.x_size = x_size
            self.y_size = y_size
            self.players = players
            self.init_boards ( 100 )
            self.move_log = [ ]  # (player,x,y,result)
            self.num_hits = 0
            self.turn = True  # True = p1, false = p2

        def init_boards ( self , ships_sum , p1_board=None , p2_board=None ):
            # tiles represented by tuples of (ship_bool,hit_bool)
            self.ships_sum = ships_sum
            self.p1_board = [ [ (0 , 0) for x in range ( self.x_size ) ] for y in range ( self.y_size ) ]
            self.p2_board = [ [ (0 , 0) for x in range ( self.x_size ) ] for y in range ( self.y_size ) ]
            self.update_boards ( p1_board , p2_board )
            return

        def update_boards ( self , p1_board=None , p2_board=None ):
            if p1_board:
                for x in range ( self.x_size ):
                    for y in range ( self.y_size ):
                        self.p1_board[ x ][ y ] = p1_board[ x ][ y ]
            elif p2_board:
                for x in range ( self.x_size ):
                    for y in range ( self.y_size ):
                        self.p2_board[ x ][ y ] = p2_board[ x ][ y ]
            return

        def hit_or_miss ( self , player , x_pos , y_pos ):
            hit = False
            if player == self.players[ 0 ]:
                if self.p2_board[ x_pos ][ y_pos ][ 0 ] == 1:  # if ship bool true
                    self.p2_board[ x_pos ][ y_pos ] = (1 , 1)
                    # set hit bool to true
                    self.num_hits += 1
                    hit = True
                self.move_log.append ( (player , x_pos , y_pos , hit) )
            elif player == self.players[ 1 ]:
                if self.p1_board[ x_pos ][ y_pos ][ 0 ] == 1:  # if ship bool true
                    self.p1_board[ x_pos ][ y_pos ] = (1 , 1)  # set hit bool to true
                    self.num_hits += 1
                    hit = True
                self.move_log.append ( (player , x_pos , y_pos , hit) )
            else:
                print ( "Tried to make move with unknown player" )
            return hit

        def won_yet ( self ):
            if self.num_hits == self.ships_sum:
                return 1
            else:
                return 0

class lobby:
    def __init__ ( self , id , p1 , p2=None ):
        self.id= id
        self.players = (p1 , p2)
        self.ready = (False,False)
        self.game = game( id,players = self.players )
        return
    def is_p1(self,name):
        if self.players[0].name == name:
            return True
        else:
            return False
    def lobby_rdy(self):
        if self.ready == (True,True):
            return True
        else:
            return False
    def add_player ( self , _player ):
        if self.players[ 1 ] == None and self.players[ 0 ] != None:
            (p1 , p2) = self.players
            self.players = (p1 , _player)
        elif self.players[ 0 ] == None and self.players[ 1 ] != None:
            (p1 , p2) = self.players
            self.players = (_player , p2)
        else:
            self.players = (_player , None)
        return

        # Simple server class to handle GET and HEAD requests
    def rdy_player(self,rdy):
        (p1 , p2) = self.ready
        if self.is_p1(rdy.name):
            p1 = not p1
            self.ready = (p1,p2)
        else:
            p2 = not p2
            self.ready = (p1,p2)

        return self.ready
    def game_start(self):
        request = []
        for player in self.players:
            c = []
            if self.is_p1(player.name):
                c.append ( game_server.make_server_request ( self.id , 'game_start' , 1 ) )
            else:
                c.append ( game_server.make_server_request ( self.id , 'game_start' , 0 ) )
            c.append (player.ip )
            c.append (player.port )
            request.append(c)
        return request

class game_server:
    def __init__ ( self , host , port , logging ):
        self.host = host
        self.port = port
        self.root_dir = 'www'
        self.logger = log.logger ( 'server' )
        self.lobbies = [] # When new person creates a game make a lobby with the game in it and the players info stored
        self.players = [] # List of players on the server? Do I need this or to store info before they join a lobby?
        self.games = {} # key = game_id, item = game object
        self.id_int = 0
        self.clients = {} # key = player name (ip,port,name,game_id,bool_p1?)
        self.turn = True # true = p1

    def make_server_request(game_id,type,msg):
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

    def get_player(self,name):
        for player in self.players:
            if player.name == name:
                return player
        return

    def get_lobby(self,id):
        for lobby in self.lobbies:
            if lobby.id == id:
                return lobby
        return

    def accept_requests ( self ):
        print("Waiting for connections")
        #conn_int = 0
        while True:

            # Change this number to change maximum number of requests
            # Conn, addr is the connection object and the address of that connection for new connections
            data , (ip,port) = self.sock.recvfrom(1024)
            if data:
                data = data.decode()
                data = js.loads(data)
                if data[ 'req_type' ] == 'connect':
                    print ( "New connection recieved from: " + str ( (ip , port) ) )
                    new_player = player(data['player'],ip,port)
                    self.players.append(new_player)
                    self.sock.sendto ( bytearray ( game_server.make_server_request ( 0 , 'conn_request' , 1 ) , "utf-8" ) ,
                                       (ip , port) )
                    #conn_int += 1 # Do I need this?
                else:
                    request = self.handle(data)
                    if request:
                        print(request)
                        # Should not need this logic block after refactoring
                        if type(request) == type([]):
                            for item in request:
                                self.sock.sendto ( bytearray (item[0] , 'utf-8' ), (item[1] ,item[2]))
                        else:
                            self.sock.sendto(bytearray(str(request),'utf-8'),(ip,port))
        return

    # Figure out if the request method is

    def handle(self,data):
        print("Recieved: " + str(data))
        _player = self.get_player(data['player'])

        if data['req_type'] == 'new_game':
            # MAKE GAME ON SERVER
            new_lobby = lobby(self.id_int,_player,None)
            self.lobbies.append(new_lobby)
            # return success message if successful
            request = game_server.make_server_request (self.id_int,'game_made',1 )
            print("Game made: "+ str(new_lobby.players[0].name))
            self.id_int += 1
            return request

        elif data['req_type'] == 'join_game':
            game_id = data['req']
            _lobby = self.get_lobby(game_id)
            if _lobby:
                new_player = self.get_player(data['player'])
                _lobby.add_player(new_player)
                # return success message if successful
                request = game_server.make_server_request(game_id,'join_result',1)
                print(str(_lobby.players))
                return request
            else:
                request = game_server.make_server_request(game_id,'join_result',0)
                return request

        elif data['req_type'] == 'move':
            (x,y) = data['req']
            game_id = data[ 'game_id' ]
            #Check to make sure its you turn/board placement is complete
            result = self.games[game_id].hit_or_miss(data['player'],x,y)
            if self.games[game_id].won_yet():
                print("Somebody won")
                request = game_server.make_server_request(game_id,'win',data['player'])
                return request
            else:
                _players = []
                request = []
                for client in self.clients.keys():
                    if self.clients[client][3] == game_id:
                        _players.append(self.clients[client])
                for p in _players:
                    c = [ ]
                    _req = game_server.make_server_request(game_id,"move_result",(result,x,y,self.turn))
                    c.append ( _req )
                    c.append(self.clients[p[2]][0])
                    c.append(self.clients[p[2]][1])
                    request.append(c)
                return request

        elif data['req_type'] == 'lobby_rdy':
            # make a lobby class to deal with lobby stuff?
            game_id = data[ 'game_id' ]
            _lobby = self.get_lobby(game_id)
            # Logic behind ready up
            (p1 , p2) = _lobby.rdy_player( _player )
            if _lobby.lobby_rdy():
                # Send request to both clients
                request = _lobby.game_start()
            else:
                if (p1,p2) == (True,False):
                    request = game_server.make_server_request ( game_id , 'player' , (True , False) )
                else:
                    request = game_server.make_server_request ( game_id , 'player' , (False , True) )
            #Logic behind ready requests
                return request
            print("Players ready: " + str(_lobby.ready))
            return request

        elif data['req_type'] == 'board_setup':
            # make the gameboard using the board sent in data
            new_board = data['req']
            game_id = data['game_id']
            _lobby = self.get_lobby ( game_id )
            if _lobby.is_p1(_player.name):
                _lobby.game.update_boards ( p1_board=new_board )
                print ( "Player 1's board updated" )
                request = game_server.make_server_request ( game_id , "move_req" , 1 )
                return request
            else:
                _lobby.game.update_boards ( p2_board=new_board )
                print ( "Player 2's board updated")
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



server = game_server ( 'localhost' , 80 , True )
server.start_server ( )
