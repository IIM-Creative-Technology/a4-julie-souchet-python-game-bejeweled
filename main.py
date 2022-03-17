import sys

import pygame
from pygame.locals import *

from src.game_engine import GameEngine
from src.utils.custom_events import *

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
        pygame.event.pump()
        # Click the close button = quit game
        if event.type == QUIT:
            loop = False
        # Mouse events handling
        elif event.type == MOUSEMOTION:
            engine.on_mouse_motion(event)
        elif event.type == MOUSEBUTTONDOWN:
            engine.on_mouse_down(event)
        # Timer handling
        elif event.type == DEBOUNCE_ALLOW:
            engine.debounce = False
        # Game start
        elif event.type == RESET:
            engine.reset()
        elif event.type == START_EASY:
            engine.start("easy", False)
        elif event.type == START_MEDIUM:
            engine.start("medium", False)
        elif event.type == START_HARD:
            engine.start("hard", False)
        elif event.type == START_INFINITE:
            engine.start("infinite", True)

print("Bye!")
pygame.quit()
sys.exit()
