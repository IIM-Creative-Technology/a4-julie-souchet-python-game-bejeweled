import sys

import pygame
from pygame.locals import *

from src.game_engine import GameEngine

pygame.init()

# Initialisation
pygame.display.set_caption("Pyjeweled")
engine = GameEngine()

# Allow only events that are relevant
pygame.event.set_allowed([
    MOUSEMOTION,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN
])

loop = True
while loop:
    # Update the game
    engine.tick()

    # Read player inputs
    for event in pygame.event.get():
        # Click the close button = quit game
        if event.type == QUIT:
            loop = False
        elif event.type == MOUSEMOTION:
            engine.handle_mouse_motion(event)
        elif event.type == MOUSEBUTTONDOWN:
            engine.handle_mouse_down(event)

pygame.quit()
sys.exit()
