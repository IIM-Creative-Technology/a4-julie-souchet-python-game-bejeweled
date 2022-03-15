from pygame import time, display, draw, Color, event

from src import screen
from src.game_grid import GameGrid
from src.utils.coordinates import from_pos_to_coord


class GameEngine:
    def __init__(self):
        self.grid = GameGrid()
        self.screen = screen.init()
        self.has_changed = False

    def tick(self):
        """Periodically updates the game state"""
        # Is the first line of the grid full?
        self.has_changed = self.grid.fill_first_line() or self.has_changed

        # Are there objects that can move?
        for column in self.grid.squares:
            for game_object in column:
                # Skip empty squares
                if game_object is not None:
                    self.has_changed = game_object.move() or self.has_changed

        if self.has_changed:
            self.draw_screen()

        time.wait(20)

    def draw_screen(self):
        """Re-draws the screen according to the current game state"""
        screen.draw_background()
        for column in self.grid.squares:
            for game_object in column:
                # Skip empty squares
                if game_object is not None:
                    # Add an indicator to show the selected object
                    if game_object.is_selected:
                        draw.rect(self.screen, Color(0, 0, 0), game_object.pos)
                    # Draw the object itself
                    screen.draw_object(game_object)
        display.flip()

    def handle_mouse_motion(self, e):
        coord = from_pos_to_coord(e.pos)
        self.has_changed = self.grid.select_square(coord)
        event.pump()

    def handle_mouse_down(self, e):
        pass
