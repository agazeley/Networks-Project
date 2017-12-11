import errno
import json as js
import socket
from pandas import DataFrame

class client:
    def __init__ ( self , host , port ):
        self.server_ip = host
        self.server_port = port
        #self.logger = log.logger('client')
        self.msg_size = 2048
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_DGRAM )

    def start_client ( self,name ):
        print ( 'connecting to ' + str(self.server_ip) + ' port ' + str(self.server_port) )
        try:
            data = self.create_request(name,'connect',1)
            self.sock.sendto (data.encode('utf-8'), (self.server_ip , self.server_port) )
        except Exception as e:
            print ( "Failed to connect to server" )
            #self.logger.log ( str ( e ) )
            #self.logger.write_log()

        serverMessage = js.loads(self.sock.recv ( 1024 ).decode())
        if serverMessage['type'] == "conn_request" and serverMessage['msg'] == 1:
            #self.GUID = serverMessage['game_id']
            return
        else:
            #self.logger.log("Failed to connect. Shutting down client")
            #self.logger.write_log()
            exit(0)

    def create_request(self,player,type,req,game_id=None):
        data = {}
        if game_id != None:
            data['game_id'] = game_id
        data['player'] = player
        data['req_type'] = type
        data['req'] = req
        data = js.dumps ( data )
        return data

    def server_request(self,data):
        self.sock.sendto(data.encode(),(self.server_ip,self.server_port))
        print("Sent: " + data)
        return

    def send_msg(self,msg):
        msg = str ( msg )
        msg = msg.encode ( )
        self.sock.sendto(msg,(self.server_ip,self.server_port))
        print("Sent " + str(msg))
        return

    def get_reply(self):
        reply = ""
        try:
            reply = self.sock.recv(self.msg_size).decode('UTF-8')
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                print('No data recieved')
                #self.logger.log(e)

            else:
                # a "real" error occurred
                print(e)
                #self.logger.log(e)
        #self.logger.write_log()
        return reply

class game:

    def __init__(self,ip,port):
        self.client_port = port
        self.client_ip = ip
        self.client = client(ip,port)
        #self.logger = log.logger("game")
        self.ships = [ 'battleship' , 'cruiser1' , 'cruiser2' , 'destroyer1' , 'destroyer2' , 'submarine1' ,
                  'submarine2' ]
        return

    def start(self):
        self.name = input("What is your name? ")
        self.client.start_client(self.name)
        request = self.client.create_request(self.name,'data',self.name)
        self.client.server_request(request)

    def print_main_menu(self):

        lobbies = js.loads ( self.client.get_reply ( ) )
        lobbies = lobbies[ 'msg' ]
        self.lobbies = lobbies

        if len(self.lobbies) > 0:
            for game_id,count in self.lobbies:
                print("Game ID: " + str(game_id) + "    Players : " + str(count))

        print ( "1. Play" )
        print ( "2. Connect" )
        return

    def print_board_menu(self):
        print("Board sizes")
        print("1. 7 X 7")
        print("2. 10 X 10")
        return

    def menu(self):
        self.print_main_menu()
        inp = True
        while inp:
            selection = self.get_integer_input("What do you want to do? ")

            if selection:
                #inp = False
                if selection == 1:
                    data = self.client.create_request(self.name,'new_game','game')
                    self.client.server_request(data)
                    reply = self.client.get_reply()
                    if reply:
                        reply = js.loads(reply)
                        if reply['msg'] == 1:
                            # Handle the reply
                            game_id= str(reply['game_id'])
                            print("Game made. Game id is: " + game_id)
                            self.game_id = int(game_id)
                            self.play()
                        else:
                            print("Failed to create game :(")
                elif selection == 2:
                    game_num = self.get_integer_input("What game number do you want to join? ")
                    data = self.client.create_request ( self.name , 'join_game' , game_num )
                    self.client.server_request ( data )
                    reply = js.loads(self.client.get_reply())
                    # Do something else in the client
                    if reply['type'] == 'join_result' and reply['msg'] == 1:
                        print("Game successfully joined")
                        self.game_id = int(reply['game_id'])
                        # Waiting for other player to start
                        self.play()
                    else:
                        print("Failed to join game")
                elif selection == 3:
                    exit(0)

    def get_board(self):
        print("Board Choice")
        while True:
            selection = self.get_integer_input("What board do you want to use? ")
            if selection == 1:
                board = []
                f = open('BS1.txt','r')
                for line in f.readlines():
                    row = []
                    line = list(map(int,line.split(',')))
                    for i in range(len(line)):
                        row.append((line[i],0))
                    board.append(row)
                return board
            elif selection == 2:
                board = [ ]
                f = open ( 'BS2.txt' , 'r' )
                for line in f.readlines ( ):
                    row = [ ]
                    line = list ( map ( int , line.split ( ',' ) ) )
                    for i in range ( len ( line ) ):
                        row.append ( (line[ i ] , 0) )
                    board.append ( row )
                return board

    def get_integer_input(self,msg):
        while True:
            cmd = input(msg)
            try:
                cmd = int(cmd)
            except Exception as e:
                print("Failed to convert to int. Try again.")
                #self.logger.log(str(e))
                #self.logger.write_log()
            finally:
                break
        return cmd

    def get_YN_input(self,msg):
        while True:
            cmd = input(msg).strip()
            cmd = cmd.lower ( )
            if cmd == "yes" or cmd == "y" or cmd == "no" or cmd == "n":
                break
        return cmd

    def get_move(self):
        while True:
            try:
                (x , y) = map(int,input ( "Enter your move: " ).split())
                if x > 6 or y > 6 or x < 0 or y < 0:
                    raise Exception("Move value out of range")
                else:
                    break
            except Exception as e:
                print(str(e))
                print("Try again.")
                #self.logger.log(str(e))
                #self.logger.write_log()
        return (x,y)

    def play ( self ):
        while True:
            ready = self.get_YN_input ( "Input 'Y' when you are ready to play " )
            if ready == 'y':
                request = self.client.create_request ( self.name , "lobby_rdy" , 1,game_id=self.game_id )
                self.client.server_request ( request )
                break
            else:
                _exit = self.get_YN_input("Do you want to exit? ")

                if _exit == 'y' or _exit == 'yes':
                    #self.logger.log("Exiting...")
                    request = self.client.create_request ( self.name , "lobby_exit" , 0 , self.game_id )
                    self.client.server_request(request)
                    self.menu()
                else:
                    print("Asking to ready up again...")

        # Wants to exit game?
        not_ready = True
        while not_ready:
            reply = js.loads ( self.client.get_reply ( ) )
            if reply['type'] == 'game_start':
                print ( "Game starting..." )
                not_ready = False
            elif reply[ 'type' ] == 'lobby_resp':
                (p1_rdy , p2_rdy) = reply[ 'msg' ]
                print ( "P1 Ready ? " + str ( p1_rdy ) + " P2 Ready ? " + str ( p2_rdy ) )

        # Game started and request for board message has been sent
        # Run ship setup
        self.opponent_board = [ [ None for x in range ( 7 ) ] for y in range ( 7 ) ]
        user_board = self.get_board()
        request = self.client.create_request(self.name,'board_setup',user_board,self.game_id)
        self.client.server_request(request)

        while True:
            reply = js.loads ( self.client.get_reply ( ) )
            if reply['type'] == 'move_req':
                (x,y) = self.get_move()
                request = self.client.create_request(self.name,'move',(x,y),self.game_id)
                self.client.server_request(request)
            elif reply['type'] == 'move_result' and reply[ 'msg' ] == 'not yet':
                print ( "Not your turn or the board has not been setup yet" )
            elif reply['type'] == 'move_result' and reply['msg'][0] == 1:
                print("Hit!")
                self.opponent_board[x][y] = True
            elif reply['type'] == 'move_result' and reply['msg'][0] == 0:
                print("Miss!")
                print("Opponents turn...")
                self.opponent_board[x][y] = False
            elif reply['type'] == 'turn':
                print(DataFrame(self.opponent_board))
                if reply['msg'][0] == 1:
                    print("Opponent hit at" + str((reply['msg'][1],reply['msg'][2])))
                    (x,y) = self.get_move()
                    request = self.client.create_request ( self.name , 'move' , (x , y) , self.game_id )
                    self.client.server_request ( request )
                else:
                    print ( "Opponent miss at" + str ( (reply[ 'msg' ][ 1 ] , reply[ 'msg' ][ 2 ]) ) )
                    (x , y) = self.get_move ( )
                    request = self.client.create_request ( self.name , 'move' , (x , y) , self.game_id )
                    self.client.server_request ( request )
            elif reply['type'] == 'win':
                print("You won!")
                request = self.client.create_request(self.name,'data',self.name)
                self.client.server_request(request)
                self.menu()
            elif reply['type'] == 'lose':
                print("You lost.")
                request = self.client.create_request(self.name, 'data', self.name)
                self.client.server_request(request)
                self.menu()
ip = input("Enter server host you want to connect to: ")
usr_client = game(ip,80)
usr_client.start()
usr_client.menu()