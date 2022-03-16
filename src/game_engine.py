import random

from pygame import time, event, mouse

from assets.settings import total_time, infinite_mode, goals
from src import screen
from src.game_grid import GameGrid
from src.game_objects.menu.game_over_overlay import GameOverOverlay
from src.sound_engine import SoundEngine
from src.utils.coordinates import from_pos_to_coord

DEBOUNCE_ALLOW = event.custom_type()


class GameEngine:
    """Handles the user's inputs and updates the game state"""

    def __init__(self):
        screen.init()
        self.sound = SoundEngine()
        self.game_over_overlay = GameOverOverlay()
        self.grid = GameGrid()
        # Settings
        self.difficulty = "medium"
        self.infinite_mode = infinite_mode
        # Internal game state
        self.has_changed = False
        self.game_over = None
        self.start_time = 0
        self.time_left = total_time.get(self.difficulty)
        self.count = 0
        self.debounce = False

    def reset(self, new_infinite_mode=infinite_mode, difficulty="easy"):
        """Resets the game state"""
        self.grid.reset()
        self.has_changed = False
        self.game_over = None
        self.count = 0
        self.start_time = time.get_ticks()
        self.time_left = total_time.get(self.difficulty)
        # Customizable settings
        self.infinite_mode = new_infinite_mode
        self.difficulty = difficulty

    def end_game(self):
        """Ends the game"""
        self.grid.clear_selection()
        if self.count < goals.get(self.difficulty):
            self.game_over = "lose"
        else:
            self.game_over = "win"
        self.sound.play(self.game_over)

    def tick(self):
        """Periodically updates the game state"""
        if not infinite_mode:
            self.time_left = self.start_time + total_time.get(self.difficulty) - time.get_ticks()

        if self.time_left <= 0:  # After game over
            if self.game_over is None:
                self.end_game()
            self.has_changed = self.update_squares() or self.has_changed
        else:  # Normal gameplay
            self.has_changed = self.grid.fill_first_line() or self.has_changed
            self.has_changed = self.update_squares() or self.has_changed

            if self.has_changed:
                self.update_selection()

        if self.has_changed:
            screen.draw_screen(
                game_over=self.game_over is not None,
                squares=self.grid.squares,
                time=self.time_left,
                overlay=self.game_over_overlay.surface,
                difficulty=self.difficulty,
                count=self.count,
            )
            self.has_changed = False
        time.wait(20)

    def on_mouse_motion(self, e):
        """Selects the group under the cursor"""
        event.pump()
        if self.game_over is None:
            coord = from_pos_to_coord(e.pos)
            self.has_changed = self.grid.select(coord)
        else:
            self.game_over_overlay.on_mouse_motion(e.pos)

    def on_mouse_down(self, e):
        """Deletes the selected group"""
        event.pump()
        if self.game_over is None:
            delete_count = self.grid.remove_selected()
            if delete_count > 0:
                self.count += delete_count
                self.sound.play("delete")
        else:
            self.game_over_overlay.click(e.pos)

    def update_squares(self) -> bool:
        """Automatically move all squares if they can be moved"""
        has_changed = False
        has_impact = False

        for column in self.grid.squares:
            for game_object in column:
                # Skip empty squares
                if game_object is not None:
                    was_moving = game_object.is_moving
                    has_changed = game_object.move() or has_changed
                    if was_moving and not game_object.is_moving:
                        has_impact = True

        # If at least one square hit bottom, play the sound fx
        if self.game_over is None and not self.debounce and has_impact:
            self.sound.play("impact")
            # Prevent the sound from playing until a delay has passed
            time.set_timer(DEBOUNCE_ALLOW, 300 + random.randint(-100, 100), 1)
            self.debounce = True

        return has_changed

    def update_selection(self):
        """Update the selection, but only if the game window has focus"""
        self.grid.clear_selection()
        if mouse.get_focused():
            coord = from_pos_to_coord(mouse.get_pos())
            self.grid.select(coord)
