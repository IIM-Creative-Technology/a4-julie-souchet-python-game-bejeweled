from pygame import display

from assets.settings import windows_width, windows_height

screen = None

def init():
    global screen
    if screen is None:
        screen = display.set_mode((windows_width, windows_height))

def draw_background():
    screen.fill((0, 0, 0))

def draw_object(object):
    print(object.image, object.pos)
    screen.blit(object.image, object.pos)
