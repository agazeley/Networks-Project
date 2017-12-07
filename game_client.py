import errno
import json as js
import pygame
import random
import socket
import inputbox

from pygame.locals import *

import log

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
DARKGRAY = (40 , 40 , 40)

# Determine what to colour each element of the game
BGCOLOR = GRAY
BUTTONCOLOR = GREEN
TEXTCOLOR = WHITE
TILECOLOR = GREEN
BORDERCOLOR = BLUE
TEXTSHADOWCOLOR = BLUE
SHIPCOLOR = YELLOW
HIGHLIGHTCOLOR = BLUE



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
            if (i + xPos > 9) or (board[ i + xPos ][ yPos ] != None) or hasAdjacent ( board , i + xPos , yPos ,
                                                                                      ship ):  # if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False , ship_coordinates)  # then return false
            else:
                ship_coordinates.append ( (i + xPos , yPos) )
    else:
        for i in range ( length ):
            if (i + yPos > 9) or (board[ xPos ][ i + yPos ] != None) or hasAdjacent ( board , xPos , i + yPos ,
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
            if (x in range ( 10 )) and (y in range ( 10 )) and (board[ x ][ y ] not in (ship , None)):
                return True
    return False

class graphics:
    def __init__(self):
        return

    def generate_default_tiles (self, default_value ):
        """
        Function generates a list of 10 x 10 tiles. The list will contain tuples
        ('shipName', boolShot) set to their (default_value).

        default_value -> boolean which tells what the value to set to
        returns the list of tuples
        """
        default_tiles = [ [ default_value ] * BOARDHEIGHT for i in range ( BOARDWIDTH ) ]

        return default_tiles
    def run_game(self):
        

        revealed_tiles = self.generate_default_tiles ( False )  # Contains the list of the tiles revealed by user
        # main board object,
        main_board = self.generate_default_tiles ( None )  # Contains the list of the ships which exists on board
        ship_objs = [ 'battleship' , 'cruiser1' , 'cruiser2' , 'destroyer1' , 'destroyer2' , 'destroyer3' ,
                      'submarine1' , 'submarine2' , 'submarine3' , 'submarine4' ]  # List of the ships available
        main_board = self.add_ships_to_board ( main_board ,
                                          ship_objs )  # call add_ships_to_board to add the list of ships to the main_board
        mousex , mousey = 0 , 0  # location of mouse
        counter = [ ]  # counter to track number of shots fired
        xmarkers , ymarkers = self.set_markers ( main_board )  # The numerical markers on each side of the board

        while True:
            # counter display (it needs to be here in order to refresh it)
            COUNTER_SURF = BASICFONT.render ( str ( len ( counter ) ) , True , WHITE )
            COUNTER_RECT = SHOTS_SURF.get_rect ( )
            COUNTER_RECT.topleft = (WINDOWWIDTH - 680 , WINDOWHEIGHT - 570)

            # Fill background
            DISPLAYSURF.fill ( BGCOLOR )

            # draw the buttons
            DISPLAYSURF.blit ( HELP_SURF , HELP_RECT )
            DISPLAYSURF.blit ( NEW_SURF , NEW_RECT )
            DISPLAYSURF.blit ( SHOTS_SURF , SHOTS_RECT )
            DISPLAYSURF.blit ( COUNTER_SURF , COUNTER_RECT )

            # Draw the tiles onto the board and their respective markers
            self.draw_board ( main_board , revealed_tiles )
            self.draw_markers ( xmarkers , ymarkers )

            mouse_clicked = False

            self.check_for_quit ( )
            # Check for pygame events
            for event in pygame.event.get ( ):
                if event.type == MOUSEBUTTONUP:
                    if HELP_RECT.collidepoint ( event.pos ):  # if the help button is clicked on
                        DISPLAYSURF.fill ( BGCOLOR )
                        self.show_help_screen ( )  # Show the help screen
                    elif NEW_RECT.collidepoint ( event.pos ):  # if the new game button is clicked on
                        self.start()  # goto main, which resets the game
                    else:  # otherwise
                        mousex , mousey = event.pos  # set mouse positions to the new position
                        mouse_clicked = True  # mouse is clicked but not on a button
                elif event.type == MOUSEMOTION:  # Detected mouse motion
                    mousex , mousey = event.pos  # set mouse positions to the new position

            # Check if the mouse is clicked at a position with a ship piece
            tilex , tiley = self.get_tile_at_pixel ( mousex , mousey )
            if tilex != None and tiley != None:
                if not revealed_tiles[ tilex ][ tiley ]:  # if the tile the mouse is on is not revealed
                    self.draw_highlight_tile ( tilex , tiley )  # draws the hovering highlight over the tile
                if not revealed_tiles[ tilex ][
                    tiley ] and mouse_clicked:  # if the mouse is clicked on the not revealed tile
                    self.reveal_tile_animation ( main_board , [ (tilex , tiley) ] )
                    revealed_tiles[ tilex ][ tiley ] = True  # set the tile to now be revealed
                    if self.check_revealed_tile ( main_board ,
                                             [ (tilex , tiley) ] ):  # if the clicked position contains a ship piece
                        left , top = self.left_top_coords_tile ( tilex , tiley )
                        self.blowup_animation ( (left , top) )
                        if self.check_for_win ( main_board , revealed_tiles ):  # check for a win
                            counter.append ( (tilex , tiley) )
                            return len ( counter )  # return the amount of shots taken
                    counter.append ( (tilex , tiley) )

            pygame.display.update ( )
            FPSCLOCK.tick ( FPS )

        return

    def add_ships_to_board ( self,board , ships ):
        """
        Function goes through a list of ships and add them randomly into a board.

        board -> list of board tiles
        ships -> list of ships to place on board
        returns list of board tiles with ships placed on certain tiles
        """
        new_board = board[ : ]
        ship_length = 0
        for ship in ships:  # go through each ship declared in the list
            # Randomly find a valid position that fits the ship
            valid_ship_position = False
            while not valid_ship_position:
                xStartpos = random.randint ( 0 , 9 )
                yStartpos = random.randint ( 0 , 9 )
                isHorizontal = random.randint ( 0 , 1 )  # vertical or horizontal positioning
                # Type of ship and their respective length
                if 'battleship' in ship:
                    ship_length = 4
                elif 'cruiser' in ship:
                    ship_length = 3
                elif 'destroyer' in ship:
                    ship_length = 2
                elif 'submarine' in ship:
                    ship_length = 1

                # check if position is valid
                valid_ship_position , ship_coords = make_ship_position ( new_board , xStartpos , yStartpos ,
                                                                         isHorizontal , ship_length , ship )
                # add the ship if it is valid
                if valid_ship_position:
                    for coord in ship_coords:
                        new_board[ coord[ 0 ] ][ coord[ 1 ] ] = ship
        return new_board
    def start(self):
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

        # Set the title in the menu bar to 'Battleship'
        pygame.display.set_caption ( 'Battleship' )
        # Keep the game running at all times
        while True:
            shots_taken = run_game ( )  # Run the game until it stops and save the result in shots_taken
            self.show_gameover_screen ( shots_taken )  # Display a gameover screen by passing in shots_taken

        return
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
    def draw_board (self, board , revealed ):
        """
        Function draws the game board.

        board -> list of board tiles
        revealed -> list of revealed tiles
        """
        # draws the grids depending on its state
        for tilex in range ( BOARDWIDTH ):
            for tiley in range ( BOARDHEIGHT ):
                left , top = self.left_top_coords_tile ( tilex , tiley )
                if not revealed[ tilex ][ tiley ]:
                    pygame.draw.rect ( DISPLAYSURF , TILECOLOR , (left , top , TILESIZE , TILESIZE) )
                else:
                    if board[ tilex ][ tiley ] != None:
                        pygame.draw.rect ( DISPLAYSURF , SHIPCOLOR , (left , top , TILESIZE , TILESIZE) )
                    else:
                        pygame.draw.rect ( DISPLAYSURF , BGCOLOR , (left , top , TILESIZE , TILESIZE) )
        # draws the horizontal lines
        for x in range ( 0 , (BOARDWIDTH + 1) * TILESIZE , TILESIZE ):
            pygame.draw.line ( DISPLAYSURF , DARKGRAY , (x + XMARGIN + MARKERSIZE , YMARGIN + MARKERSIZE) ,
                               (x + XMARGIN + MARKERSIZE , WINDOWHEIGHT - YMARGIN) )
        # draws the vertical lines
        for y in range ( 0 , (BOARDHEIGHT + 1) * TILESIZE , TILESIZE ):
            pygame.draw.line ( DISPLAYSURF , DARKGRAY , (XMARGIN + MARKERSIZE , y + YMARGIN + MARKERSIZE) ,
                               (WINDOWWIDTH - (DISPLAYWIDTH + MARKERSIZE * 2) , y + YMARGIN + MARKERSIZE) )
    def set_markers (self, board ):
        """
        Function creates the lists of the markers to the side of the game board which indicates
        the number of ship pieces in each row and column.

        board: list of board tiles
        returns the 2 lists of markers with number of ship pieces in each row (xmarkers)
            and column (ymarkers)
        """
        xmarkers = [ 0 for i in range ( BOARDWIDTH ) ]
        ymarkers = [ 0 for i in range ( BOARDHEIGHT ) ]
        # Loop through the tiles
        for tilex in range ( BOARDWIDTH ):
            for tiley in range ( BOARDHEIGHT ):
                if board[ tilex ][ tiley ] != None:  # if the tile is a ship piece, then increment the markers
                    xmarkers[ tilex ] += 1
                    ymarkers[ tiley ] += 1

        return xmarkers , ymarkers
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
    def draw_highlight_tile (self, tilex , tiley ):
        """
        Function draws the hovering highlight over the tile.

        tilex -> int; x position of tile
        tiley -> int; y position of tile
        """
        left , top = self.left_top_coords_tile ( tilex , tiley )
        pygame.draw.rect ( DISPLAYSURF , HIGHLIGHTCOLOR , (left , top , TILESIZE , TILESIZE) , 4 )
    def check_for_keypress (self):
        """
        Function checks for any key presses by pulling out all KEYDOWN and KEYUP events from queue.

        returns any KEYUP events, otherwise return None
        """
        for event in pygame.event.get ( [ KEYDOWN , KEYUP , MOUSEBUTTONDOWN , MOUSEBUTTONUP , MOUSEMOTION ] ):
            if event.type in (KEYDOWN , MOUSEBUTTONUP , MOUSEBUTTONDOWN , MOUSEMOTION):
                continue
            return event.key
        return None
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
                                                   ' the edges of the game board tell you how' , BASICFONT ,
                                                   TEXTCOLOR )
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

    def __init__(self,ip,port):
        self.client_port = port
        self.client_ip = ip
        self.client = client(ip,port)
        self.logger = log.logger("game")
        self.ships = [ 'battleship' , 'cruiser1' , 'cruiser2' , 'destroyer1' , 'destroyer2' , 'submarine1' ,
                  'submarine2' ]
        return

    def start(self):
        self.name = input ( "What is your name? " )
        self.client.start_client(self.name)
        request = self.client.create_request(self.name,'data',self.name)
        self.client.server_request(request)

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
                request = self.client.create_request ( self.name , "lobby_rdy" , self.name,game_id=self.game_id )
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
            if reply['type'] == 'game_start':
                print ( "Game starting..." )
                not_ready = False
            elif reply[ 'type' ] == 'lobby_rdy':
                (p1_rdy , p2_rdy) = reply[ 'msg' ]
                print ( "P1 Ready ? " + str ( p1_rdy ) + "P2 Ready ? " + str ( p2_rdy ) )

        # Game started and request for board message has been sent
        # Run ship setup
        self.opponent_board = [ [ None for x in range ( 7 ) ] for y in range ( 7 ) ]
        user_board = self.generate_board(self.opponent_board,self.ships)
        request = self.client.create_request(self.name,'board_setup',user_board,self.game_id)
        self.client.server_request(request)
        victorious = False
        while not victorious:
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
                if reply['msg'] == self.name:
                    print("You won!")
                else:
                    print("You lost!")
                victorious = False

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

usr_client = game('localhost',80)
usr_client.start()
usr_client.menu()

