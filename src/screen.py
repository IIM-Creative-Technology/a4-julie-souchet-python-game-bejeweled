from typing import Optional

from pygame import display, draw, Surface, SRCALPHA

from assets.settings import windows_width, windows_height, select_color, background_color, grid_width, total_time, \
    timer_width, overlay_background_color

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


def draw_timer(time: float):
    # TODO change progress bar color according to time left
    rect = (
        grid_width + 20,  # left
        windows_height * (total_time - time) / total_time,  # top: goes down
        timer_width,  # width
        windows_height * time / total_time,  # height: diminishes
    )  # bottom stays constant at the bottom of the screen
    draw.rect(screen, select_color, rect)


def draw_overlay():
    overlay = Surface((windows_width, windows_height), SRCALPHA)  # alpha in pixels
    overlay.fill(overlay_background_color)
    screen.blit(overlay, (0, 0))
