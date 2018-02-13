# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

class inputbox:
    def __init__(self,x,y):
        self.screen = pygame.display.set_mode((x,y))

    def get_key(self):
      while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
          return event.key
        else:
          pass

    def display_box(self, message):
      "Print a message in a box in the middle of the screen"
      fontobject = pygame.font.Font(None,18)
      pygame.draw.rect(self.screen, (0,0,0),
                       ((self.screen.get_width() / 2) - 100,
                        (self.screen.get_height() / 2) - 10,
                        200,20), 0)
      pygame.draw.rect(self.screen, (255,255,255),
                       ((self.screen.get_width() / 2) - 102,
                        (self.screen.get_height() / 2) - 12,
                        204,24), 1)
      if len(message) != 0:
        self.screen.blit(fontobject.render(message, 1, (255,255,255)),
                    ((self.screen.get_width() / 2) - 100, (self.screen.get_height() / 2) - 10))
      pygame.display.flip()

    def ask(self, question):
      "ask(screen, question) -> answer"
      q = question
      pygame.font.init()
      current_string = []
      question = question + ": " + "".join(current_string)
      self.display_box(question)
      while 1:
        question = q
        inkey = self.get_key()
        if inkey == K_BACKSPACE:
          current_string = current_string[0:-1]
        elif inkey == K_RETURN:
          break
        elif inkey == K_MINUS:
          current_string.append("_")
        elif inkey <= 127:
          current_string.append(chr(inkey))
        question = question + ": " + "".join ( current_string )
        self.display_box( question)
      return "".join(current_string)

inp = inputbox(400,200)
reply = inp.ask("What is your name")
print(str(reply))