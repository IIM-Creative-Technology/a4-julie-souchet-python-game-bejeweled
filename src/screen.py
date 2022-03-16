from typing import Optional

from pygame import display, draw, Surface, Rect, font

from assets.settings import windows_width, windows_height, select_color, background_color, grid_width, total_time, \
    progress_bar_width, infinite_mode, goal_reached_color, goal_not_reached_color, goals, goal_hints

screen: Optional[Surface] = None
font.init()
main_font = font.SysFont("Arial", 12)
title_font = font.Font("assets/HomemadeApple-Regular.ttf", 36)


def init():
    global screen
    if screen is None:
        if not infinite_mode:
            width = windows_width
        else:
            width = grid_width
        screen = display.set_mode((width, windows_height))


def draw_screen(game_over, squares, time, overlay, difficulty, count):
    """Re-draws the screen according to the current game state"""
    # TODO only redraw parts that have changed
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
        draw_timer(time, total_time.get(difficulty))
        draw_goal(count, difficulty)

    display.flip()


def draw_background():
    screen.fill(background_color)


def draw_object(game_object):
    # Add an indicator to show the selected object
    if game_object.is_selected:
        draw.rect(screen, select_color, game_object.pos)
    # Draw the object itself
    screen.blit(game_object.image, game_object.pos)


def draw_timer(time: float, total: int):
    # TODO change progress bar color according to time left
    if not infinite_mode:
        rect = (
            grid_width + 20 + progress_bar_width,  # left
            windows_height * (total - time) / total,  # top: goes down
            progress_bar_width,  # width
            windows_height * time / total,  # height: diminishes
        )  # bottom stays constant at the bottom of the screen
        draw.rect(screen, select_color, rect)


def draw_goal(count, difficulty):
    goal_nb = goals.get(difficulty)
    goal_height = goal_hints.get(difficulty)

    # Progress bar
    height = count * goal_height / goal_nb
    rect = Rect(
        grid_width + 10,  # left
        windows_height - height,  # top
        progress_bar_width,  # width
        max(windows_height, height)  # height: max prevents overflow
    )

    if count < goal_nb:
        color = goal_not_reached_color
    else:
        color = goal_reached_color
    draw.rect(screen, color, rect)

    # Goal hint
    line = Rect(
        rect.left - 2,  # left
        windows_height - goal_height,  # top
        progress_bar_width + 6,  # width
        3  # height
    )
    draw.rect(screen, "black", line)

    # Goal hint text
    text = main_font.render(f"{count} / {goal_nb}", True, "black")
    screen.blit(text, (line.left - 3, line.top - text.get_rect().height))
