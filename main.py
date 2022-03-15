import sys
import pygame
from pygame.locals import *

from assets.settings import *
from src import screen
from src.GameObject import GameObject

pygame.init()

# Open window
pygame.display.set_caption("Pyjeweled")
# Init screen
screen.init()

loop = True
objects = [
    GameObject("assets/red.png", (0, 0)),
    GameObject("assets/green.png", (50, 50)),
    GameObject("assets/yellow.png", (100, 100))
]
while loop:
    for event in pygame.event.get():
        # Draw background
        screen.draw_background()
        # TODO TODELETE
        for object in objects:
            object.move()
            screen.draw_object(object)

        pygame.display.flip()

        # Click the close button = quit game
        if event.type is QUIT:
            loop = False

pygame.quit()
sys.exit()
