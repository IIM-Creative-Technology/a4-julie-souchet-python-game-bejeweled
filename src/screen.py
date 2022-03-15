from pygame import display, draw, Color

from assets.settings import windows_width, windows_height

screen = None


def init():
    global screen
    if screen is None:
        screen = display.set_mode((windows_width, windows_height))


def draw_background():
    screen.fill((255, 255, 255))


def draw_object(game_object):
    # Add an indicator to show the selected object
    if game_object.is_selected:
        draw.rect(screen, Color(0, 0, 0), game_object.pos)
    # Draw the object itself
    screen.blit(game_object.image, game_object.pos)
