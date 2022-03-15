import sys
import pygame
from pygame.locals import *

from assets.settings import *

pygame.init()

# Open window
screen = pygame.display.set_mode((windows_width, windows_height))
pygame.display.set_caption("Pyjeweled")

loop = True
while loop:
    for event in pygame.event.get():
        # Draw background
        screen.fill((0, 0, 0))
        print(event)
        # Click the close button = quit game
        if event.type is QUIT:
            loop = False

pygame.quit()