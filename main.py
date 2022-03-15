import sys

import pygame
from pygame.locals import *

from src import screen
from src.GameEngine import GameEngine

pygame.init()

# Initialisation
pygame.display.set_caption("Pyjeweled")
screen.init()
engine = GameEngine()

loop = True
while loop:
    # Update the game
    engine.tick()

    # Read player inputs
    for event in pygame.event.get():
        # Click the close button = quit game
        if event.type is QUIT:
            loop = False

pygame.quit()
sys.exit()
