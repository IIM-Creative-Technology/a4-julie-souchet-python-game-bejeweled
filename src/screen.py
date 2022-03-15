from pygame import display

from assets.settings import windows_width, windows_height

screen = None


def init():
    global screen
    if screen is None:
        screen = display.set_mode((windows_width, windows_height))
    return screen


def draw_background():
    screen.fill((255, 255, 255))


def draw_object(game_object):
    screen.blit(game_object.image, game_object.pos)
