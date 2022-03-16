from pygame import time, event, mouse, QUIT

from assets.settings import total_time, infinite_mode
from src import screen
from src.game_grid import GameGrid
from src.utils.coordinates import from_pos_to_coord


class GameEngine:
    def __init__(self):
        screen.init()
        self.grid = GameGrid()
        self.has_changed = False
        self.time_left = total_time
        self.game_over = False

    def tick(self):
        """Periodically updates the game state"""
        if self.time_left == 0:  # After game over
            if not self.game_over:
                self.end_game()
            self.has_changed = self.update_squares() or self.has_changed
        else:  # Normal gameplay
            if not infinite_mode:
                self.time_left -= 10

            self.has_changed = self.grid.fill_first_line() or self.has_changed
            self.has_changed = self.update_squares() or self.has_changed

            if self.has_changed:
                self.update_selection()

        if self.has_changed:
            screen.draw_screen(self.game_over, self.grid.squares, self.time_left)
            self.has_changed = False
        time.wait(20)

    def handle_mouse_motion(self, e):
        """Selects the group under the cursor"""
        event.pump()
        if not self.game_over:
            coord = from_pos_to_coord(e.pos)
            self.has_changed = self.grid.select(coord)

    def handle_mouse_down(self):
        """Deletes the selected group"""
        event.pump()
        if not self.game_over:
            self.grid.remove_selected()

    def update_squares(self) -> bool:
        has_changed = False
        for column in self.grid.squares:
            for game_object in column:
                # Skip empty squares
                if game_object is not None:
                    has_changed = game_object.move() or has_changed
        return has_changed

    def update_selection(self):
        """Update the selection, but only if the game window has focus"""
        self.grid.clear_selection()
        if mouse.get_focused():
            coord = from_pos_to_coord(mouse.get_pos())
            self.grid.select(coord)

    def end_game(self):
        """Ends the game, blocks controls"""
        self.game_over = True
        event.set_allowed(QUIT)
        self.grid.clear_selection()
