import game_server
import socket
import time
import json as js
import sys
import log
from game_server import game_server
from server_game import game
import threading as thread

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