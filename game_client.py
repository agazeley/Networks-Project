import socket
import log
import json as js
import errno

class client:
    def __init__ ( self , host , port ):
        self.server_ip = host
        self.server_port = port
        self.logger = log.logger('client')
        self.msg_size = 2048
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )

    def start_client ( self ):
        print ( 'connecting to %s port ' + str(self.server_port) )
        try:
            self.sock.connect ( (self.server_ip , self.server_port) )
        except Exception as e:
            print ( "Failed to connect to server" )
            self.logger.log ( str ( e ) )
            self.logger.write_log()

        serverMessage = self.sock.recv ( 1024 ).decode()
        if serverMessage == "Connection successful":
            return
        else:
            self.logger.log("Failed to connect. Shutting down client")
            self.logger.write_log()
            exit(0)

    def run(self):
        while True:
            msg = input ( "Send a message: " )
            size = len ( msg )
            msg = msg.encode ( )
            self.sock.sendall ( msg )
            reply = self.sock.recv ( self.msg_size ).decode ( 'UTF-8' )
            if reply:
                print ( "Received: " + str ( reply ) )
        return

    def create_request(self,player,type,req,game_id=None):
        data = {}
        if game_id:
            data['game_id'] = game_id
        data['player'] = player
        data['req_type'] = type
        data['req'] = req
        data = js.dumps ( data )
        return data

    def server_request(self,data):
        self.send_msg(data)
        return

    def send_msg(self,msg):
        msg = str ( msg )
        msg = msg.encode ( )
        self.sock.sendall(msg)
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
                self.logger.log(e)

            else:
                # a "real" error occurred
                print(e)
                self.logger.log(e)
        self.logger.write_log()
        return reply

class game:

    def __init__(self,ip,port):
        self.client_port = port
        self.client_ip = ip
        self.client = client(ip,port)
        self.logger = log.logger("game")
        return

    def start(self):
        self.client.start_client()
        self.name = input("What is your name? ")

    def print_main_menu(self):
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
                            # Do something in the client
                        else:
                            print("Failed to create game :(")
                elif selection == 2:
                    game_num = self.get_integer_input("What game number do you want to join? ")
                    data = self.client.create_request ( self.name , 'join_game' , game_num )
                    self.client.server_request ( data )
                    reply = js.loads(self.client.get_reply())
                    # Do something else in the client
                    if reply['join_result'] == 1:
                        print("Game successfully joined")
                        self.game_id = game_id
                        # Waiting for other player to start
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
                    line = list(map(int,line.split(",")))
                    board.append(line)
                return board
            elif selection == 2:
                board = [ ]
                f = open ( 'BS1.txt' , 'r' )
                for line in f.readlines ( ):
                    line = list ( map ( int , line.split ( "," ) ) )
                    board.append ( line )
                return board

    def get_integer_input(self,msg):
        while True:
            cmd = input(msg)
            try:
                cmd = int(cmd)
            except Exception as e:
                print("Failed to convert to int. Try again.")
                self.logger.log(str(e))
                self.logger.write_log()
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
            except Exception as e:
                print("Try again.")
                self.logger.log(str(e))
                self.logger.write_log()
            finally:
                break
        return (x,y)

    def play ( self ):
        while True:
            ready = self.get_YN_input ( "Input 'Y' when youre ready to play" )
            if ready == 'y':
                request = self.client.create_request ( self.name , "lobby_rdy" , self.name )
                self.client.server_request ( request )
                break
            else:
                _exit = self.get_YN_input("Do you want to exit? ")
                if _exit == 'y' or _exit == 'yes':
                    self.logger.log("Exiting...")
                    exit(0)
                else:
                    print("Asking to ready up again...")

        # Wants to exit game?
        not_ready = True
        while not_ready:
            reply = js.loads ( self.client.get_reply ( ) )
            for key in reply.keys ( ):
                if key == 'game_start':
                    print ( "Game starting..." )
                    not_ready = False
                elif key == 'player':
                    (p1_rdy , p2_rdy) = reply[ 'msg' ]
                    print ( "P1 Ready ? " + str ( p1_rdy ) + "P2 Ready ? " + str ( p2_rdy ) )
        # Game started and request for board message has been sent
        # Run ship setup
        user_board = self.get_board()
        request = self.client.create_request(self.name,'board_setup',user_board,self.game_id)
        self.client.server_request(request)
        victorious = False
        while not victorious:
            # print options for board types
            # create board
            # send board info to server
            # mae moves
            # check if won game
            # next players turn
            self.opponent_board = [[ 0 for x in range(7)] for y in range(7)]
            (x,y) = self.get_move()
            request = self.client.create_request(self.name,'move',(x,y))
            reply = js.loads ( self.client.get_reply ( ) )
            if reply['type'] == 'move_result' and reply[ 'msg' ] == 'not yet':
                print ( "Not your turn or the board has not been setup yet" )
            elif reply['type'] == 'move_result' and reply['msg'] == True:
                print("Hit!")
                self.opponent_board[x][y] = 1
            elif reply['type'] == 'move_result' and reply['msg'] == False:
                print("Miss!")
                print("Opponents turn...")
                # Need wait for move function

        return

usr_client = game('localhost',80)
usr_client.start()
usr_client.menu()

