import errno
import json as js
import pygame
import random
import socket
import random , sys , pygame
from pygame.locals import *
import log
from textbox import TextBox


# Set variables, like screen width and height
# globals
FPS = 30  # Determines the number of frames per second
REVEALSPEED = 8  # Determines the speed at which the squares reveals after being clicked
WINDOWWIDTH = 800  # Width of game window
WINDOWHEIGHT = 600  # Height of game window
TILESIZE = 40  # Size of the squares in each grid(tile)
MARKERSIZE = 40  # Size of the box which contatins the number that indicates how many ships in this row/col
BUTTONHEIGHT = 20  # Height of a standard button
BUTTONWIDTH = 40  # Width of a standard button
TEXT_HEIGHT = 25  # Size of the text
TEXT_LEFT_POSN = 10  # Where the text will be positioned
BOARDWIDTH = 10  # Number of grids horizontally
BOARDHEIGHT = 10  # Number of grids vertically
DISPLAYWIDTH = 200  # Width of the game board
EXPLOSIONSPEED = 10  # How fast the explosion graphics will play

XMARGIN = int ( (WINDOWWIDTH - (
BOARDWIDTH * TILESIZE) - DISPLAYWIDTH - MARKERSIZE) / 2 )  # x-position of the top left corner of board
YMARGIN = int (
    (WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE) - MARKERSIZE) / 2 )  # y-position of the top left corner of board

# Colours which will be used by the game
BLACK = (0 , 0 , 0)
WHITE = (255 , 255 , 255)
GREEN = (0 , 204 , 0)
GRAY = (60 , 60 , 60)
BLUE = (0 , 50 , 255)
YELLOW = (255 , 255 , 0)
LIGHT_YELLOW = (200,200,0)
DARKGRAY = (40 , 40 , 40)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
RED = (200,0,0)

# Determine what to colour each element of the game
BGCOLOR = GRAY
BUTTONCOLOR = GREEN
TEXTCOLOR = WHITE
TILECOLOR = GREEN
BORDERCOLOR = BLUE
TEXTSHADOWCOLOR = BLUE
SHIPCOLOR = YELLOW
HIGHLIGHTCOLOR = BLUE

global DISPLAYSURF , FPSCLOCK , BASICFONT , HELP_SURF , HELP_RECT , NEW_SURF , NEW_RECT , SHOTS_SURF , SHOTS_RECT , BIGFONT , COUNTER_SURF , COUNTER_RECT , HBUTTON_SURF , EXPLOSION_IMAGES
pygame.init ( )
FPSCLOCK = pygame.time.Clock ( )
# Fonts used by the game
DISPLAYSURF = pygame.display.set_mode ( (WINDOWWIDTH , WINDOWHEIGHT) )
BASICFONT = pygame.font.Font ( 'freesansbold.ttf' , 20 )
BIGFONT = pygame.font.Font ( 'freesansbold.ttf' , 50 )

# Create and label the buttons
HELP_SURF = BASICFONT.render ( "HELP" , True , WHITE )
HELP_RECT = HELP_SURF.get_rect ( )
HELP_RECT.topleft = (WINDOWWIDTH - 180 , WINDOWHEIGHT - 350)
NEW_SURF = BASICFONT.render ( "NEW GAME" , True , WHITE )
NEW_RECT = NEW_SURF.get_rect ( )
NEW_RECT.topleft = (WINDOWWIDTH - 200 , WINDOWHEIGHT - 200)

# The 'Shots:' label at the top
SHOTS_SURF = BASICFONT.render ( "Shots: " , True , WHITE )
SHOTS_RECT = SHOTS_SURF.get_rect ( )
SHOTS_RECT.topleft = (WINDOWWIDTH - 750 , WINDOWHEIGHT - 570)

# Load the explosion graphics from the /img folder
EXPLOSION_IMAGES = [ pygame.image.load ( "img/blowup1.png" ) , pygame.image.load ( "img/blowup2.png" ) ,
    pygame.image.load ( "img/blowup3.png" ) , pygame.image.load ( "img/blowup4.png" ) ,
    pygame.image.load ( "img/blowup5.png" ) , pygame.image.load ( "img/blowup6.png" ) ]

def make_ship_position ( board , xPos , yPos , isHorizontal , length , ship ):
    """
    Function makes a ship on a board given a set of variables

    board -> list of board tiles
    xPos -> x-coordinate of first ship piece
    yPos -> y-coordinate of first ship piece
    isHorizontal -> True if ship is horizontal
    length -> length of ship
    returns tuple: True if ship position is valid and list ship coordinates
    """
    ship_coordinates = [ ]  # the coordinates the ship will occupy
    if isHorizontal:
        for i in range ( length ):
            if (i + xPos > 6) or (board[ i + xPos ][ yPos ] != None) or hasAdjacent ( board , i + xPos , yPos ,
                                                                                      ship ):  # if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False , ship_coordinates)  # then return false
            else:
                ship_coordinates.append ( (i + xPos , yPos) )
    else:
        for i in range ( length ):
            if (i + yPos > 6) or (board[ xPos ][ i + yPos ] != None) or hasAdjacent ( board , xPos , i + yPos ,
                                                                                      ship ):  # if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False , ship_coordinates)  # then return false
            else:
                ship_coordinates.append ( (xPos , i + yPos) )
    return (True , ship_coordinates)

def hasAdjacent ( board , xPos , yPos , ship ):
    """
    Funtion checks if a ship has adjacent ships

    board -> list of board tiles
    xPos -> x-coordinate of first ship piece
    yPos -> y-coordinate of first ship piece
    ship -> the ship being checked for adjacency
    returns true if there are adjacent ships and false if there are no adjacent ships
    """
    for x in range ( xPos - 1 , xPos + 2 ):
        for y in range ( yPos - 1 , yPos + 2 ):
            if (x in range ( 7 )) and (y in range ( 7 )) and (board[ x ][ y ] not in (ship , None)):
                return True
    return False


class client:
    def __init__ ( self , host , port ):
        self.server_ip = host
        self.server_port = port
        self.logger = log.logger('client')
        self.msg_size = 2048
        self.sock = socket.socket ( socket.AF_INET , socket.SOCK_DGRAM )

    def start_client ( self,name ):
        print ( 'connecting to ' + str(self.server_ip) + ' port ' + str(self.server_port) )
        try:
            data = self.create_request(name,'connect',1)
            self.sock.sendto (data.encode('utf-8'), (self.server_ip , self.server_port) )
        except Exception as e:
            print ( "Failed to connect to server" )
            self.logger.log ( str ( e ) )
            self.logger.write_log()

        serverMessage = js.loads(self.sock.recv ( 1024 ).decode())
        if serverMessage['type'] == "conn_request" and serverMessage['msg'] == 1:
            self.GUID = serverMessage['game_id']
            return
        else:
            self.logger.log("Failed to connect. Shutting down client")
            self.logger.write_log()
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
                self.logger.log(e)

            else:
                # a "real" error occurred
                print(e)
                self.logger.log(e)
        self.logger.write_log()
        return reply

class game:

    def __init__(self,ip,port,):
        self.client_port = port
        self.client_ip = ip
        self.client = client(ip,port)
        self.logger = log.logger("game")
        self.ships = [ 'battleship' , 'cruiser1' , 'cruiser2' , 'destroyer1' , 'destroyer2' , 'submarine1' ,
                  'submarine2' ]

        return

    def start(self):
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

    def get_lobbies(self):
        lobbies = js.loads ( self.client.get_reply ( ) )
        lobbies = lobbies[ 'msg' ]
        self.lobbies = lobbies
        if len(self.lobbies) > 0:
            for game_id,count in self.lobbies:
                print("Game ID: " + str(game_id) + "    Players : " + str(count))
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
                if x > 6 or y > 6 or x < 0 or y < 0:
                    raise Exception("Move value out of range")
                else:
                    break
            except Exception as e:
                print(str(e))
                print("Try again.")
                self.logger.log(str(e))
                self.logger.write_log()
        return (x,y)

    def play ( self ):
        while True:
            ready = self.get_YN_input ( "Input 'Y' when youre ready to play " )
            if ready == 'y':
                request = self.client.create_request ( self.name , "lobby_rdy" , self.name,game_id=self.game_id )
                self.client.server_request ( request )
                break
            else:
                _exit = self.get_YN_input("Do you want to exit? ")

                if _exit == 'y' or _exit == 'yes':
                    self.logger.log("Exiting...")
                    request = self.client.create_request ( self.name , "lobby_exit" , 1 , self.game_id )
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
            elif reply[ 'type' ] == 'lobby_rdy':
                (p1_rdy , p2_rdy) = reply[ 'msg' ]
                print ( "P1 Ready ? " + str ( p1_rdy ) + "P2 Ready ? " + str ( p2_rdy ) )

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
                self.opponent_board[x][y] = (1,1)
            elif reply['type'] == 'move_result' and reply['msg'][0] == 0:
                print("Miss!")
                print("Opponents turn...")
                self.opponent_board[x][y] = (0,1)
            elif reply['type'] == 'turn':
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
                break
            elif reply['type'] == 'lose':
                print("You lost.")
                break
        self.menu()
        return

    def generate_board(self,board,ships):
        new_board = board[:]
        ship_length = 0
        for ship in ships:
            valid_ship_position = False
            while not valid_ship_position:
                x_start_pos = random.randint(0,6)
                y_start_pos = random.randint(0,6)
                is_horizontal = random.randint(0,1)

                if 'battleship' in ship:
                    ship_length = 4
                elif 'cruiser' in ship:
                    ship_length = 3
                elif 'destroyer' in ship:
                    ship_length = 2
                elif 'submarine' in ship:
                    ship_length = 1
                valid_ship_position, ship_coords = make_ship_position(new_board,x_start_pos,y_start_pos,is_horizontal,ship_length,ship)
                if valid_ship_position:
                    for coord in ship_coords:
                        new_board[ coord[ 0 ] ][ coord[ 1 ] ] = ship
        return new_board

    def show_gameover_screen (self, shots_fired ):
        """
        Function display a gameover screen when the user has successfully shot at every ship pieces.

        shots_fired -> the number of shots taken before game is over
        """
        DISPLAYSURF.fill ( BGCOLOR )
        titleSurf , titleRect = self.make_text_objs ( 'Congrats! Puzzle solved in:' , BIGFONT , TEXTSHADOWCOLOR )
        titleRect.center = (int ( WINDOWWIDTH / 2 ) , int ( WINDOWHEIGHT / 2 ))
        DISPLAYSURF.blit ( titleSurf , titleRect )

        titleSurf , titleRect = self.make_text_objs ( 'Congrats! Puzzle solved in:' , BIGFONT , TEXTCOLOR )
        titleRect.center = (int ( WINDOWWIDTH / 2 ) - 3 , int ( WINDOWHEIGHT / 2 ) - 3)
        DISPLAYSURF.blit ( titleSurf , titleRect )

        titleSurf , titleRect = self.make_text_objs ( str ( shots_fired ) + ' shots' , BIGFONT , TEXTSHADOWCOLOR )
        titleRect.center = (int ( WINDOWWIDTH / 2 ) , int ( WINDOWHEIGHT / 2 + 50 ))
        DISPLAYSURF.blit ( titleSurf , titleRect )

        titleSurf , titleRect = self.make_text_objs ( str ( shots_fired ) + ' shots' , BIGFONT , TEXTCOLOR )
        titleRect.center = (int ( WINDOWWIDTH / 2 ) - 3 , int ( WINDOWHEIGHT / 2 + 50 ) - 3)
        DISPLAYSURF.blit ( titleSurf , titleRect )

        pressKeySurf , pressKeyRect = self.make_text_objs ( 'Press a key to try to beat that score.' , BASICFONT ,
                                                       TEXTCOLOR )
        pressKeyRect.center = (int ( WINDOWWIDTH / 2 ) , int ( WINDOWHEIGHT / 2 ) + 100)
        DISPLAYSURF.blit ( pressKeySurf , pressKeyRect )

        while self.check_for_keypress ( ) == None:  # Check if the user has pressed keys, if so start a new game
            pygame.display.update ( )
            FPSCLOCK.tick ( )


class graphics:

    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.x = 10
        self.y = 10
        self.colors = {}
        self.colors['black'] = (0,0,0)
        self.colors['white'] = (255,255,255)
        self.colors['red'] = (255,0,0)
        self.colors['green'] = (0,255,0)
        self.colors['blue'] = (0,0,255)
        self.game_display = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption("BATTLESHIP!")
        self.clock = pygame.time.Clock()
        self.pboard = None
        self.game_logic = game
        self.reply = False

    def text_objects (self, text , font ):
        textSurface = font.render ( text , True , BLACK )
        return textSurface , textSurface.get_rect ( )

    # msg = Text on button, x is starting x, y is starting y,
    # w is width, h is height, ic is initial color, ac is hover color
    def button (self, msg , x , y , w , h , ic , ac,action=None,args=None ):
        mouse = pygame.mouse.get_pos ( )
        clicked = pygame.mouse.get_pressed()

        if x + w > mouse[ 0 ] > x and y + h > mouse[ 1 ] > y:
            pygame.draw.rect ( self.game_display , ac , (x , y , w , h) )

            if clicked[0] == 1 and action != None:
                action() # run action function
        else:
            pygame.draw.rect ( self.game_display , ic , (x , y , w , h) )

        smallText = pygame.font.Font ( "freesansbold.ttf" , 20 )
        textSurf , textRect = self.text_objects ( msg , smallText )
        textRect.center = ((x + (w / 2)) , (y + (h / 2)))
        self.game_display.blit ( textSurf , textRect)

    def get_name(self,id,final):
        usr_client.name = final
        print(usr_client.name)
        return
    def connect_to_game(self):
        if not self.reply:
            usr_client.start()
            usr_client.get_lobbies()
            self.reply = True
        return

    def game_intro(self):
        settings = {"command": self.get_name , "inactive_on_enter": False , }

        self.inp_box = TextBox ( rect=(350 , 300 , 150 , 30),**settings )

        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.inp_box.get_event(event)

            self.game_display.fill(WHITE)

            largeText = pygame.font.Font ( 'freesansbold.ttf' , 65 )
            TextSurf , TextRect = self.text_objects ( "Battleship: Main Menu" , largeText )
            TextRect.center = ((self.display_width / 2) , (self.display_height / 6))
            self.game_display.blit ( TextSurf , TextRect )

            mouse = pygame.mouse.get_pos()
            #Position buttons here
            self.button ( "What is your name? " , 250 , 250 , 200 , 50 , RED , RED )
            self.button ( "Start!" , 150 , 150 , 100 , 50 , GREEN , BRIGHT_GREEN,self.game_loop)
            self.button ( "Connect" , 350 , 150 , 100 , 50 , LIGHT_YELLOW ,YELLOW,self.connect_to_game )
            self.button ( "Quit!" , 550 , 150 , 100 , 50 , RED , BRIGHT_RED,quit)

            self.inp_box.update()
            self.inp_box.draw(self.game_display)

            pygame.display.update ( )
            FPSCLOCK.tick(FPS )

    def blowup_animation (self, coord ):
        """
        Function creates the explosition played if a ship is shot.

        coord -> tuple of tile coords to apply the blowup animation
        """
        for image in EXPLOSION_IMAGES:  # go through the list of images in the list of pictures and play them in sequence
            # Determine the location and size to display the image
            image = pygame.transform.scale ( image , (TILESIZE + 10 , TILESIZE + 10) )
            DISPLAYSURF.blit ( image , coord )
            pygame.display.flip ( )
            FPSCLOCK.tick ( EXPLOSIONSPEED )  # Determine the delay to play the image with

    def check_revealed_tile (self, board , tile ):
        """
        Function checks if a tile location contains a ship piece.

        board -> the tiled board either a ship piece or none
        tile -> location of tile
        returns True if ship piece exists at tile location
        """
        return board[ tile[ 0 ][ 0 ] ][ tile[ 0 ][ 1 ] ] != None

    def reveal_tile_animation (self, board , tile_to_reveal ):
        """
        Function creates an animation which plays when the mouse is clicked on a tile, and whatever is
        behind the tile needs to be revealed.

        board -> list of board tile tuples ('shipName', boolShot)
        tile_to_reveal -> tuple of tile coords to apply the reveal animation to
        """
        for coverage in range ( TILESIZE , (-REVEALSPEED) - 1 , -REVEALSPEED ):  # Plays animation based on reveal speed
            self.draw_tile_covers ( board , tile_to_reveal , coverage )

    def draw_tile_covers (self, board , tile , coverage ):
        """
        Function draws the tiles according to a set of variables.

        board -> list; of board tiles
        tile -> tuple; of tile coords to reveal
        coverage -> int; amount of the tile that is covered
        """
        left , top = self.left_top_coords_tile ( tile[ 0 ][ 0 ] , tile[ 0 ][ 1 ] )
        if self.check_revealed_tile ( board , tile ):
            pygame.draw.rect ( DISPLAYSURF , SHIPCOLOR , (left , top , TILESIZE , TILESIZE) )
        else:
            pygame.draw.rect ( DISPLAYSURF , BGCOLOR , (left , top , TILESIZE , TILESIZE) )
        if coverage > 0:
            pygame.draw.rect ( DISPLAYSURF , TILECOLOR , (left , top , coverage , TILESIZE) )

        pygame.display.update ( )
        FPSCLOCK.tick ( FPS )

    def show_help_screen (self):
        """
        Function display a help screen until any button is pressed.
        """
        line1_surf , line1_rect = self.make_text_objs ( 'Press a key to return to the game' , BASICFONT , TEXTCOLOR )
        line1_rect.topleft = (TEXT_LEFT_POSN , TEXT_HEIGHT)
        DISPLAYSURF.blit ( line1_surf , line1_rect )

        line2_surf , line2_rect = self.make_text_objs ( 'This is a battleship puzzle game. Your objective is ' \
                                                   'to sink all the ships in as few' , BASICFONT , TEXTCOLOR )
        line2_rect.topleft = (TEXT_LEFT_POSN , TEXT_HEIGHT * 3)
        DISPLAYSURF.blit ( line2_surf , line2_rect )

        line3_surf , line3_rect = self.make_text_objs ( 'shots as possible. The markers on' \
                                                   ' the edges of the game board tell you how' , BASICFONT , TEXTCOLOR )
        line3_rect.topleft = (TEXT_LEFT_POSN , TEXT_HEIGHT * 4)
        DISPLAYSURF.blit ( line3_surf , line3_rect )

        line4_surf , line4_rect = self.make_text_objs ( 'many ship pieces are in each' \
                                                   ' column and row. To reset your game click on' , BASICFONT ,
                                                   TEXTCOLOR )
        line4_rect.topleft = (TEXT_LEFT_POSN , TEXT_HEIGHT * 5)
        DISPLAYSURF.blit ( line4_surf , line4_rect )

        line5_surf , line5_rect = self.make_text_objs ( 'the "New Game" button.' , BASICFONT , TEXTCOLOR )
        line5_rect.topleft = (TEXT_LEFT_POSN , TEXT_HEIGHT * 6)
        DISPLAYSURF.blit ( line5_surf , line5_rect )

        while self.check_for_keypress ( ) == None:  # Check if the user has pressed keys, if so go back to the game
            pygame.display.update ( )
            FPSCLOCK.tick ( )

    def draw_highlight_tile (self, tilex , tiley ):
        """
        Function draws the hovering highlight over the tile.

        tilex -> int; x position of tile
        tiley -> int; y position of tile
        """
        left , top = self.left_top_coords_tile ( tilex , tiley )
        pygame.draw.rect ( DISPLAYSURF , HIGHLIGHTCOLOR , (left , top , TILESIZE , TILESIZE) , 4 )

    def get_tile_at_pixel (self, x , y ):
        """
        Function finds the corresponding tile coordinates of pixel at top left, defaults to (None, None) given a coordinate.

        x -> int; x position of pixel
        y -> int; y position of pixel
        returns tuple (tilex, tiley)
        """
        for tilex in range ( BOARDWIDTH ):
            for tiley in range ( BOARDHEIGHT ):
                left , top = self.left_top_coords_tile ( tilex , tiley )
                tile_rect = pygame.Rect ( left , top , TILESIZE , TILESIZE )
                if tile_rect.collidepoint ( x , y ):
                    return (tilex , tiley)
        return (None , None)

    def check_for_quit (self):
        """
        Function checks if the user has attempted to quit the game.
        """
        for event in pygame.event.get ( QUIT ):
            pygame.quit ( )
            sys.exit ( )

    def draw_markers (self, xlist , ylist ):
        """
        Function draws the two list of markers to the side of the board.
        xlist -> list of row markers
        ylist -> list of column markers
        """
        for i in range ( len ( xlist ) ):  # Draw the x-marker list
            left = i * MARKERSIZE + XMARGIN + MARKERSIZE + (TILESIZE / 3)
            top = YMARGIN
            marker_surf , marker_rect = self.make_text_objs ( str ( xlist[ i ] ) , BASICFONT , TEXTCOLOR )
            marker_rect.topleft = (left , top)
            DISPLAYSURF.blit ( marker_surf , marker_rect )
        for i in range ( len ( ylist ) ):  # Draw the y-marker list
            left = XMARGIN
            top = i * MARKERSIZE + YMARGIN + MARKERSIZE + (TILESIZE / 3)
            marker_surf , marker_rect = self.make_text_objs ( str ( ylist[ i ] ) , BASICFONT , TEXTCOLOR )
            marker_rect.topleft = (left , top)
            DISPLAYSURF.blit ( marker_surf , marker_rect )

    def draw_board(self,board,reveal):
        for tilex in range(self.x):
            for tiley in range(self.y):
                left, top = self.left_top_coords_tile(tilex,tiley)
                if not reveal[tilex][tiley]:
                    pygame.draw.rect(DISPLAYSURF,TILECOLOR,(left,top,TILESIZE,TILESIZE))
                else:
                    if board[ tilex ][ tiley ] != None:
                        pygame.draw.rect ( DISPLAYSURF , SHIPCOLOR , (left , top , TILESIZE , TILESIZE) )
                    else:
                        pygame.draw.rect ( DISPLAYSURF , BGCOLOR , (left , top , TILESIZE , TILESIZE) )
        for x in range(0,(BOARDWIDTH+1)*TILESIZE,TILESIZE):
            pygame.draw.line(DISPLAYSURF,DARKGRAY,(x+XMARGIN + MARKERSIZE, YMARGIN + MARKERSIZE),(x + XMARGIN+MARKERSIZE,WINDOWHEIGHT- YMARGIN))
        for y in range(0,(BOARDHEIGHT+1)*TILESIZE,TILESIZE):
            pygame.draw.line ( DISPLAYSURF , DARKGRAY , (XMARGIN + MARKERSIZE , y + YMARGIN + MARKERSIZE) ,
                               (WINDOWWIDTH - (DISPLAYWIDTH + MARKERSIZE * 2) , y + YMARGIN + MARKERSIZE) )

    def left_top_coords_tile(self, tilex , tiley ):
        """
        Function calculates and returns the pixel of the tile in the top left corner

        tilex -> int; x position of tile
        tiley -> int; y position of tile
        returns tuple (int, int) which indicates top-left pixel coordinates of tile
        """
        left = tilex * TILESIZE + XMARGIN + MARKERSIZE
        top = tiley * TILESIZE + YMARGIN + MARKERSIZE
        return (left , top)

    def set_markers(self):
        xmarkers = [i for i in range(self.x)]
        ymarkers = [i for i in range(self.y)]
        return xmarkers,ymarkers

    def message_display(self,text):
        large_text = pygame.font.Font('freesanbold.ttf',115)
        TextSurf,TextRect = self.text_objects(text,large_text)
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.game_display.blit(TextSurf,TextRect)
        pygame.display.update()
        self.game_loop()

    def generate_default_tiles (self, default_value ):
        """
        Function generates a list of 10 x 10 tiles. The list will contain tuples
        ('shipName', boolShot) set to their (default_value).

        default_value -> boolean which tells what the value to set to
        returns the list of tuples
        """
        default_tiles = [ [ default_value ] * self.y for i in range ( self.x ) ]

        return default_tiles

    def make_text_objs (self, text , font , color ):
        """
        Function creates a text.

        text -> string; content of text
        font -> Font object; face of font
        color -> tuple of color (red, green blue); colour of text
        returns the surface object, rectangle object
        """
        surf = font.render ( text , True , color )
        return surf , surf.get_rect ( )

    def game_loop ( self ):
        main_board = self.generate_default_tiles ( None )
        self.revealed = self.generate_default_tiles ( False )
        mousex , mousey = 0 , 0
        self.counter = [ ]
        xmarkers , ymarkers = self.set_markers ( )
        won = False
        while True:
            COUNTER_SURF = BASICFONT.render ( str ( len ( self.counter ) ),True,WHITE )
            COUNTER_RECT = SHOTS_SURF.get_rect ( )
            COUNTER_RECT.topleft = (self.x - 680 , self.y - 570)

            DISPLAYSURF.fill ( BGCOLOR )

            DISPLAYSURF.blit ( HELP_SURF , HELP_RECT )
            DISPLAYSURF.blit ( NEW_SURF , NEW_RECT )
            DISPLAYSURF.blit ( SHOTS_SURF , SHOTS_RECT )
            DISPLAYSURF.blit ( COUNTER_SURF , COUNTER_RECT )

            self.draw_board ( main_board , self.revealed )
            self.draw_markers ( xmarkers , ymarkers )
            mouse_clicked = False

            self.check_for_quit ( )

            #Get the loop events
            for event in pygame.event.get ( ):
                if event.type == MOUSEBUTTONUP:
                    if HELP_RECT.collidepoint ( event.pos ):
                        DISPLAYSURF.fill ( BGCOLOR )
                        self.show_help_screen ( )
                    elif NEW_RECT.collidepoint ( event.pos ):
                        # Reset to menu somehow
                        print ( "Reset Clicked" )
                    else:
                        mousex , mousey = event.pos
                        mouse_clicked = True
                elif event.type == MOUSEMOTION:
                    mousex , mousey = event.pos

            tilex , tiley = self.get_tile_at_pixel ( mousex , mousey )
            if tilex != None and tiley != None:
                if not self.revealed[ tilex ][ tiley ]:
                    self.draw_highlight_tile ( tilex , tiley )
                if not self.revealed[ tilex ][ tiley ] and mouse_clicked:
                    self.reveal_tile_animation ( main_board , [ (tilex , tiley) ] )
                    self.revealed[ tilex ][ tiley ] = True
                    if self.check_revealed_tile ( main_board , [ (tilex , tiley) ] ):
                        left , top = self.left_top_coords_tile ( tilex , tiley )
                        self.blowup_animation ( (left , top) )
                        if won:
                            self.counter.append ( (tilex , tiley) )
                            return len ( self.counter )
                    self.counter.append ( (tilex , tiley) )

            self.button ( "Quit!" , 600 , 450 , 100 , 50 , LIGHT_YELLOW , YELLOW , self.game_intro )
            pygame.display.update ( )
            FPSCLOCK.tick ( FPS )





usr_client = game('localhost',80)
_graphics = graphics()
_graphics.game_intro()

