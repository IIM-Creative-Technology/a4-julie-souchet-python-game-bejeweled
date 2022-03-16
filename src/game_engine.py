from pygame import time, display, event, mouse

from src import screen
from src.game_grid import GameGrid
from src.utils.coordinates import from_pos_to_coord


class GameEngine:
    def __init__(self):
        screen.init()
        self.grid = GameGrid()
        self.has_changed = False

    def tick(self):
        """Periodically updates the game state"""
        # Is the first line of the grid full yet?
        self.has_changed = self.grid.fill_first_line() or self.has_changed

        # Are there objects that can move?
        for column in self.grid.squares:
            for game_object in column:
                # Skip empty squares
                if game_object is not None:
                    self.has_changed = game_object.move() or self.has_changed

        if self.has_changed:
            # Update the selection, only if the game window has focus
            self.clear_selection()
            if mouse.get_focused():
                coord = from_pos_to_coord(mouse.get_pos())
                self.grid.select_square(coord)
            self.draw_screen()

        self.has_changed = False
        time.wait(20)

    def draw_screen(self):
        """Re-draws the screen according to the current game state"""
        screen.draw_background()
        for column in self.grid.squares:
            for game_object in column:
                # Skip empty squares
                if game_object is not None:
                    screen.draw_object(game_object)
        display.flip()

    def handle_mouse_motion(self, e):
        """Selects the group under the cursor"""
        event.pump()
        coord = from_pos_to_coord(e.pos)
        self.has_changed = self.grid.select_square(coord)

    def handle_mouse_down(self):
        """Deletes the selected group"""
        event.pump()
        self.remove_selected()

    def remove_selected(self):
        # If there is no selection -> ignore
        if self.grid.selected_squares.__len__() == 0:
            return

        for square in self.grid.selected_squares:
            coord = from_pos_to_coord(square.pos)
            self.grid.set_square(coord, None)
        self.grid.selected_squares.clear()

    def clear_selection(self):
        # If there is no selection -> ignore
        if self.grid.selected_squares.__len__() == 0:
            return

        for square in self.grid.selected_squares:
            square.is_selected = False
        self.grid.selected_squares.clear()
