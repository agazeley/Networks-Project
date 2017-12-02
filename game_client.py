import socket
import log
import json as js


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

    def create_request(self,player,type,req):
        data = {}
        data['player'] = player
        data['req_type'] = type
        data['req'] = req
        data = js.dumps ( data )
        return data

    def server_request(self,data):
        self.send_msg(data)
        return self.get_reply()

    def send_msg(self,msg):
        msg = str ( msg )
        msg = msg.encode ( )
        self.sock.sendall(msg)
        print("Sent " + str(msg))
        return

    def get_reply(self):
        reply = self.sock.recv(self.msg_size).decode('UTF-8')
        return  reply

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
            selection = self.get_integer_input("What do you want to do?")

            if selection:
                #inp = False
                if selection == 1:
                    data = self.client.create_request(self.name,'cmd','game')
                    reply = self.client.server_request(data)
                    # Do something in the client
                elif selection == 2:
                    data = self.client.create_request ( self.name , 'cmd' , 'connect' )
                    reply = self.client.server_request ( data )
                    # Do something else in the client
                elif selection == 3:
                    exit(0)

    def get_integer_input(self,msg):
        while True:
            cmd = input(msg)
            try:
                cmd = int(cmd)
            except Exception as e:
                print("Failed to conver to int. Try again.")
                self.logger.log(str(e))
                self.logger.write_log()
            finally:
                break
        return cmd


    def play(self):
        victorious = False
        while not victorious:
            self.print_board_menu()
            selection = self.get_integer_input("What board do you want to use? ")

            # print options for board types
            # create board
            # send board info to server
            # mae moves
            # check if won game
            # next players turn
            #
        return

usr_client = game('localhost',50001)
usr_client.start()
usr_client.menu()

