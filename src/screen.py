from typing import Optional

from pygame import display, draw, Surface

from assets.settings import windows_width, windows_height, select_color, background_color

screen: Optional[Surface] = None


def init():
    global screen
    if screen is None:
        screen = display.set_mode((windows_width, windows_height))


def draw_background():
    screen.fill(background_color)


def draw_object(game_object):
    # Add an indicator to show the selected object
    if game_object.is_selected:
        draw.rect(screen, select_color, game_object.pos)
    # Draw the object itself
    screen.blit(game_object.image, game_object.pos)
