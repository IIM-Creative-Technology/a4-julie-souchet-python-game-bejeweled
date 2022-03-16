from pygame import time, event, mouse, QUIT

from assets.settings import total_time, infinite_mode
from src import screen
from src.game_grid import GameGrid
from src.game_objects.menu.game_over_overlay import GameOverOverlay
from src.sound_engine import SoundEngine
from src.utils.coordinates import from_pos_to_coord


class GameEngine:
    """Handles the user's inputs and updates the game state"""

    def __init__(self):
        screen.init()
        self.sound = SoundEngine()
        self.game_over_overlay = GameOverOverlay()
        self.grid = GameGrid()
        self.has_changed = False
        self.game_over = False
        self.time_left = total_time
        self.infinite_mode = infinite_mode

    def reset(self, new_time_left=total_time, new_infinite_mode=infinite_mode):
        """Resets the game state"""
        self.grid.reset()
        self.has_changed = False
        self.game_over = False
        # Customizable settings
        self.time_left = new_time_left
        self.infinite_mode = new_infinite_mode

    def end_game(self):
        """Ends the game, blocks controls"""
        self.sound.play("win")
        self.game_over = True
        event.set_allowed(QUIT)
        self.grid.clear_selection()

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
            screen.draw_screen(
                game_over=self.game_over,
                squares=self.grid.squares,
                time=self.time_left,
                overlay=self.game_over_overlay.surface
            )
            self.has_changed = False
        time.wait(20)

    def on_mouse_motion(self, e):
        """Selects the group under the cursor"""
        event.pump()
        if not self.game_over:
            coord = from_pos_to_coord(e.pos)
            self.has_changed = self.grid.select(coord)
        else:
            self.game_over_overlay.on_mouse_motion(e.pos)

    def on_mouse_down(self, e):
        """Deletes the selected group"""
        event.pump()
        if not self.game_over:
            did_delete = self.grid.remove_selected()
            if did_delete:
                self.sound.play("delete")
        else:
            self.game_over_overlay.click(e.pos)

    def update_squares(self) -> bool:
        """Automatically move all squares if they can be moved"""
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
