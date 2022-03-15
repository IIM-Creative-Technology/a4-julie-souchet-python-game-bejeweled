from pygame import time, display

from src import screen
from src.game_grid import GameGrid


class GameEngine:
    def __init__(self):
        self.grid = GameGrid()
        screen.init()

    def tick(self):
        """Periodically updates the game state"""
        # Is the first line of the grid full?
        has_changed = self.grid.fill_first_line()

        # Are there objects that can move?
        for column in self.grid.squares:
            for item in column:
                # Skip empty squares
                if item is not None:
                    has_changed = item.move() or has_changed

        if has_changed:
            self.draw_screen()

        time.wait(20)

    def draw_screen(self):
        """Re-draws the screen according to the current game state"""
        screen.draw_background()
        for column in self.grid.squares:
            for item in column:
                # Skip empty squares
                if item is not None:
                    screen.draw_object(item)
        display.flip()
