from typing import Optional

from pygame import display, draw, Surface

from assets.settings import windows_width, windows_height, select_color, background_color, grid_width, total_time, \
    timer_width, infinite_mode

screen: Optional[Surface] = None


def init():
    global screen
    if screen is None:
        if not infinite_mode:
            width = windows_width
        else:
            width = grid_width
        screen = display.set_mode((width, windows_height))


def draw_screen(game_over, squares, time, overlay):
    """Re-draws the screen according to the current game state"""
    draw_background()
    for column in squares:
        for game_object in column:
            # Skip empty squares
            if game_object is not None:
                draw_object(game_object)

    # Add game over overlay if necessary
    if game_over:
        screen.blit(overlay, (0, 0))
    else:
        draw_timer(time)

    display.flip()


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
    if not infinite_mode:
        rect = (
            grid_width + 20,  # left
            windows_height * (total_time - time) / total_time,  # top: goes down
            timer_width,  # width
            windows_height * time / total_time,  # height: diminishes
        )  # bottom stays constant at the bottom of the screen
        draw.rect(screen, select_color, rect)
