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
        self.name = input("What is your name?")

    def menu(self):
        print ( "1. Play" )
        print ( "2. Connect" )
        inp = True
        while inp:
            selection = self.get_menu_input()

            if selection:
                #inp = False
                if selection == 1:
                    data = {}
                    data[ 'cmd' ] = 'game'
                    data[ 'msg' ] = selection
                    data = js.dumps ( data )
                    self.client.send_msg(data)
                    reply = self.client.get_reply()
                    print(reply)
                    # Do something in the client
                elif selection == 2:
                    data = {}
                    data['cmd'] = 'connect'
                    data['msg'] = selection
                    data = js.dumps(data)
                    self.client.send_msg ( data )

                    reply = self.client.sock.recv ( self.client.msg_size ).decode ( 'UTF-8' )
                    print(reply)
                    # Do something else in the client
                elif selection == 3:
                    exit(0)

    def get_menu_input(self):
        while True:
            cmd = input("What do you want to do? ")
            try:
                cmd = int(cmd)
            except Exception as e:
                print("Failed to conver to int. Try again.")
                self.logger.log(str(e))
                self.logger.write_log()
            finally:
                break
        return cmd


usr_client = game('localhost',50001)
usr_client.start()
usr_client.menu()

