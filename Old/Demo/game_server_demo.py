import socket
import json as js
import sys

# Program: Game Server for  Server-Client Battleship
# Final Project for CS313
# Author: Andrew Gazeley

class player:
    # params
    # name:string
    # ip: string
    # port: int
    # optional board: list<list<(int,int)>>
    def __init__(self,name,ip,port,board=None):
        self.name = name
        self.ready = False
        self.ip = ip
        self.port = port
        self.board = board
        self.num_hits = 0
        return

class game:

        # params
        # _player1: player
        # _player2: player
        # id: int
        # x_siz: int
        # y_size: int
        def __init__ ( self ,_player1,_player2, id=0 , x_size=7 , y_size=7 ,  ):
            self.game_id = id
            self.x_size = x_size
            self.y_size = y_size
            self.player1 = _player1
            self.player2 = _player2
            self.init_boards ( 10 )
            self.move_log = [ ]  # (player,x,y,result)
            self.turn = True  # True = p1, false = p2

        # makes blank boards and sets up win condition, updates the board with user inputed boards
        # params
        # ships_sum: int
        # p1_board: list<list<(int,int)>>
        # p2_board: list<list<(int,int)>>
        def init_boards ( self , ships_sum , p1_board=None , p2_board=None ):
            # tiles represented by tuples of (ship_bool,hit_bool)
            self.ships_sum = ships_sumv
            self.p1_board = [ [ (0 , 0) for x in range ( self.x_size ) ] for y in range ( self.y_size ) ]
            self.p2_board = [ [ (0 , 0) for x in range ( self.x_size ) ] for y in range ( self.y_size ) ]
            self.update_boards ( p1_board , p2_board )
            return

        # p1_board: list<list<(int,int)>>
        # p2_board: list<list<(int,int)>>
        def update_boards ( self , p1_board=None , p2_board=None ):
            if p1_board:
                self.p1_board = p1_board
            elif p2_board:
                self.p2_board = p2_board
            return

        # processes hit or miss
        # params
        # _player: player
        # x_pos: int
        # y_ pos: int
        # returns bool
        def hit_or_miss ( self , _player , x_pos , y_pos ):
            hit = False
            if self.move_log.count((_player,x_pos,y_pos)) > 0:
                print("YOU MADE THIS MOVE ALREADY DUMMY. MISS")
                return False
            if _player == self.player1:
                if self.p2_board[ x_pos ][ y_pos ][ 0 ] == 1:  # if ship bool true
                    self.p2_board[ x_pos ][ y_pos ] = (1 , 1)
                    # set hit bool to true
                    self.player1.num_hits += 1
                    hit = True
                self.move_log.append ( (player , x_pos , y_pos , hit) )
            elif _player == self.player2:
                if self.p1_board[ x_pos ][ y_pos ][ 0 ] == 1:  # if ship bool true
                    self.p1_board[ x_pos ][ y_pos ] = (1 , 1)  # set hit bool to true
                    self.player2.num_hits += 1
                    hit = True
                self.move_log.append ( (player , x_pos , y_pos , hit) )
            else:
                print("WHY ARE WE HERE")
                hit = False
            return hit

        # checks if a player has met the win conditions
        # param
        # _player: player
        # returns 1/0
        def won_yet(self, _player):
            # if _player.num_hits == self.ships_sum:
            if _player.num_hits == 3:
                return 1
            else:
                return 0

class lobby:
    # creates lobby with id and initial player
    # params
    # id: int
    # p1: player
    # optional p2: player
    def __init__ ( self , id , p1 , p2=None ):
        self.id = id
        self.player1 = p1
        self.player2 = p2
        self.ready = (False,False)
        self.game = None
        return

    # checks if a players name is p1 on the server
    # param
    # name: string
    # returns bool
    def is_p1(self,name):
        if self.player1.name == name:
            return True
        else:
            return False

    # checks lobby conditions
    def lobby_rdy(self):
        if self.ready == (True,True):
            return True
        else:
            return False

    # adds player to the lobby if possible
    # param
    # _player: player
    def add_player ( self , _player ):
        if self.player2 == None:
            self.player2 = _player
        elif self.player1 == None and self.player2 != None:
            self.player1 = _player
        return

    # returns int
    # of players in a lobby
    def get_players(self):
        if self.player1 != None and self.player2 != None:
            return 2
        else:
            return 1

    # removes player from the lobby
    # param
    # _player: player
    def remove_player(self,_player):
        if self.player1 == _player:
            self.player1 = None
            (p1,p2) = self.ready
            self.ready = (False,p2)
        elif self.player2 == _player:
            self.player2 == None
            (p1 , p2) = self.ready
            self.ready = (p1 , False)
        return

    # packages game won requests to proper players
    # params
    # _player: player
    # game_id: int
    # returns list<string>
    def game_won(self,_player,game_id):
        request = []
        for p in [self.player1,self.player2]:
            c = []
            if _player == p:
                c.append( game_server.make_server_request ( game_id , 'win' , p.name ))
            else:
                c.append((game_server.make_server_request(game_id,'lose',p.name)))
            c.append(p.ip)
            c.append(p.port)
            request.append(c)
        return request

    # creates a game in the lobby with players
    # used after both players ready up
    # params
    # player1: player
    # player2: player
    def make_game(self,player1,player2):
        self.game = game (player1,player2,self.id)
        return

    # readys up a player in the current lobby
    # param
    # _player: player
    # return (bool,bool)
    def rdy_player(self,_player):
        (p1 , p2) = self.ready
        if self.is_p1(rdy.name):
            p1 = not p1
            self.ready = (p1,p2)
        else:
            p2 = not p2
            self.ready = (p1,p2)

        return self.ready

    # starts a game and sends start requests with first turn data
    # return string
    def game_start(self):
        if self.player1 != None and self.player2 != None:
            self.make_game(self.player1,self.player2)
            request = []
            for player in [self.player1,self.player2]:
                c = []
                if self.is_p1(player.name):
                    c.append ( game_server.make_server_request ( self.id , 'game_start' , 1 ) )
                else:
                    c.append ( game_server.make_server_request ( self.id , 'game_start' , 0 ) )
                c.append (player.ip )
                c.append (player.port )
                request.append(c)
            return request
        else:
            print(str((self.player1,self.player2)))
            return

    # packages move made data into requests to be sent out
    # params:
    # x: int
    # y: int
    # _player: player
    # result: bool/int
    # return string
    def move_made(self,x,y,_player,result):
        request = []
        for p in [self.player1,self.player2]:
            c = []
            if p == _player:
                c.append(game_server.make_server_request(self.id,'move_result',(result,x,y)))
            else:
                c.append(game_server.make_server_request(self.id,'turn',(result,x,y)))
            c.append(p.ip)
            c.append(p.port)
            request.append(c)
        return request

class game_server:
    # params
    # host: string
    # port: int
    def __init__ ( self , host , port):
        self.host = host
        self.port = port
        self.lobbies = {} # key = game_id, item = lobby  When new person creates a game make a lobby with the game in it and the players info stored
        self.players = [] # List of players on the server? Do I need this or to store info before they join a lobby?
        self.id_int = 0

    # packages server request
    # params
    # game_id: int
    # type: string
    # msg: object
    # returns string
    def make_server_request(game_id,type,msg):
        data = {}
        data['game_id'] =game_id
        data['type'] = type
        data['msg'] = msg
        data = js.dumps(data)
        return data

    # starts server up on give host:port config
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
                #self.logger.log ( "Failed to bind sockets for ports " + str ( user_port ) + " and 8080. " )
                self.shutdown ( )
                sys.exit ( 1 )
        print ( "Server running on " + self.host + ":" + str ( self.port ) )
        #self.logger.log ( "Server running on " + self.host + ":" + str ( self.port ) )
        self.accept_requests ( )
        #self.logger.write_log ( )

    # gracefully shuts down the server
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

    # sends a string to the connected socket.
    # OBSOLETE
    def send_msg(self,msg):
        msg = str(msg)
        msg = msg.encode()
        self.sock.sendall(msg)
        print("Sent" + str(msg))
        return

    # finds a player in list of connections and returns him
    # param
    # name: string
    # return: player
    def get_player(self,name):
        for _player in self.players:
            if _player.name == name:
                return _player
        return

    # deletes a player from a specific game
    # params
    # game_id: int
    # _player: player
    def remove_player_from_lobby(self,game_id,_player):
        _lobby = self.lobbies[game_id]
        _lobby.remove_player(_player)
        if _lobby.id == game_id:
            if _lobby.player1 == _player:
                if _lobby.player2 == None:
                     del self.lobbies[game_id]
            else:
                if _lobby.player1 == None:
                    del self.lobbies[game_id]
        return

    # deletes a lobby
    # param
    # game_id: int
    def remove_lobby(self,game_id):
        print("Deleting lobby " + str(game_id))
        del self.lobbies[game_id]
        return

    # packages lobby info
    # returns list<(int,int)>
    def get_lobbies(self):
        _lobbies = []
        for key in self.lobbies.keys ( ):
            c = self.lobbies[key].get_players()
            _lobbies.append ( (self.lobbies[ key ].id , c) )
        return _lobbies

    # gets a lobby on id
    # param
    # id: int
    # return: lobby
    def get_lobby(self,id):
        return self.lobbies[id]

    # accepts new connections and handles requests to server
    # sends data to multiple clients based off handle() function
    def accept_requests ( self ):
        print("Waiting for connections")
        #conn_int = 0
        while True:

            # Change this number to change maximum number of requests
            # Conn, addr is the connection object and the address of that connection for new connections
            data , (ip,port) = self.sock.recvfrom(2048)
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

    # huge massive handler function
    # param
    # data: dictionary
    # returns string or nothing
    def handle(self,data):
        print("Recieved: " + str(data))
        _player = self.get_player(data['player'])

        # new game protocol
        if data['req_type'] == 'new_game':
            # MAKE GAME ON SERVER
            new_lobby = lobby(self.id_int,_player,None)
            self.lobbies[self.id_int] = new_lobby
            # return success message if successful
            request = game_server.make_server_request (self.id_int,'game_made',1 )
            print("Game made: "+ str(new_lobby.player1.name))
            self.id_int += 1
            return request

        # lobby data request protocol
        elif data['req_type'] == 'data':
            _lobbies = self.get_lobbies()
            request = game_server.make_server_request(0,'lobby_data',_lobbies)
            print(request)
            return request

        # join game request protocol and logic
        elif data['req_type'] == 'join_game':
            game_id = data['req']
            _lobby = self.lobbies[game_id]
            if _lobby and _lobby.get_players() != 2:
                new_player = self.get_player(data['player'])
                _lobby.add_player(new_player)
                # return success message if successful
                request = game_server.make_server_request(game_id,'join_result',1)
                print(str((_lobby.player1.name,_lobby.player2.name)))
                return request
            else:
                request = game_server.make_server_request(game_id,'join_result',0)
                return request

        # move request and logic handles victory conditions
        elif data['req_type'] == 'move':
            (x,y) = data['req']
            game_id = data[ 'game_id' ]
            result = self.lobbies[game_id].game.hit_or_miss(_player,x,y)
            #Check to make sure its you turn/board placement is complete
            if self.lobbies[game_id].game.won_yet(_player):
                print("Somebody won")
                request = self.lobbies[game_id].game_won(_player,game_id)
                self.remove_lobby(game_id)
            else:
                request = self.lobbies[game_id].move_made(x,y,_player,result)
            return request

        # exit lobby protocol and logic
        elif data['req_type'] == 'lobby_exit':
            game_id = data['game_id']
            self.remove_player_from_lobby(game_id,_player)
            _lobbies = self.get_lobbies()
            request = game_server.make_server_request ( game_id , 'lobby_data' , _lobbies )
            return request

        # lobby ready protocol and logic
        elif data['req_type'] == 'lobby_rdy':
            # make a lobby class to deal with lobby stuff?
            if data['req'] == 1:
                game_id = data[ 'game_id' ]
                _lobby = self.get_lobby(game_id)
                # Logic behind ready up
                (p1 , p2) = _lobby.rdy_player( _player )
                if _lobby.lobby_rdy():
                    # Send request to both clients
                    request = _lobby.game_start()
                else:
                    if (p1,p2) == (True,False):
                        request = game_server.make_server_request ( game_id , 'lobby_resp' , (True , False) )
                    else:
                        request = game_server.make_server_request ( game_id , 'lobby_resp' , (False , True) )
                #Logic behind ready requests
                print("Players ready: " + str(_lobby.ready))
                return request
            elif data['req'] == 0:
                # remove player from game
                game_id = data['game_id']
                _lobby = self.get_lobby(game_id)
                _lobby.remove_player(_player.name)

        # board setup request
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

# main
server = game_server ( 'localhost' , 80 )
server.start_server ( )
