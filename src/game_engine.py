import random

from pygame import time, mouse

from src import screen
from src.game_grid import GameGrid
from src.game_objects.menu.game_over_overlay import GameOverOverlay
from src.game_objects.menu.start_overlay import StartOverlay
from src.settings import total_time, goals
from src.sound_engine import SoundEngine
from src.utils.coordinates import from_pos_to_coord
from src.utils.custom_events import *


class GameEngine:
    """Handles the user's inputs and updates the game state"""

    def __init__(self):
        screen.init()
        self.sound = SoundEngine()
        self.game_over_overlay = None
        self.start_overlay = StartOverlay()
        self.grid = GameGrid()
        # Settings
        self.difficulty = None
        self.is_infinite = None
        # Internal game state
        self.count = 0
        self.debounce = False
        self.game_over = None
        self.goal = goals.get(self.difficulty)
        self.has_changed = True
        self.has_started = False
        self.start_time = 0
        self.time_left = total_time.get(self.difficulty)

    def reset(self):
        """Resets the game state"""
        # Internal game state
        self.count = 0
        self.debounce = False
        self.game_over = None
        self.has_changed = True
        self.has_started = False

    def start(self, difficulty, is_infinite=False):
        print(f"Started game on {difficulty} (infinite={is_infinite})")
        self.grid.reset()
        # Customizable settings
        self.difficulty = difficulty
        self.is_infinite = is_infinite
        # Internal game state
        self.goal = goals.get(self.difficulty)
        self.has_started = True
        self.start_time = time.get_ticks()
        self.time_left = total_time.get(self.difficulty)

    def end_game(self):
        """Ends the game"""
        self.grid.clear_selection()
        if self.count < self.goal:
            self.game_over = "lose"
        else:
            self.game_over = "win"
        self.sound.play(self.game_over)
        self.game_over_overlay = GameOverOverlay(self.count >= self.goal)

    def tick(self):
        """Periodically updates the game state"""
        time.wait(20)
        overlay = None
        if not self.has_started:
            overlay = self.start_overlay.surface
        else:
            if not self.is_infinite:  # Normal gameplay
                self.time_left = self.start_time + total_time.get(self.difficulty) - time.get_ticks()

                if self.time_left <= 0:  # After game over
                    if self.game_over is None:
                        self.end_game()
                    overlay = self.game_over_overlay.surface
                    self.has_changed = self.update_squares() or self.has_changed

            self.has_changed = self.grid.fill_first_line() or self.has_changed
            self.has_changed = self.update_squares() or self.has_changed

            if self.has_changed:
                self.update_selection()

        if self.has_changed:
            screen.draw_screen(
                squares=self.grid.squares,
                time=self.time_left,
                overlay=overlay,
                difficulty=self.difficulty,
                count=self.count,
                goal=self.goal,
                is_infinite=self.is_infinite
            )
            self.has_changed = False

    def on_mouse_motion(self, e):
        """Selects the group under the cursor"""
        if not self.has_started:  # start menu
            self.start_overlay.on_mouse_motion(e.pos)
        elif self.game_over is None:  # main game
            coord = from_pos_to_coord(e.pos)
            self.has_changed = self.grid.select(coord)
        else:  # game over menu
            self.game_over_overlay.on_mouse_motion(e.pos)

    def on_mouse_down(self, e):
        """Deletes the selected group"""
        if not self.has_started:  # start menu
            self.start_overlay.click(e.pos)
        elif self.game_over is None:  # main game
            delete_count = self.grid.remove_selected()
            if delete_count > 0:
                self.count += delete_count
                self.sound.play("delete")
                if not self.is_infinite:  # normal mode: add time to the timer
                    time_bonus = delete_count * 125  # + 1/8th second for each deleted
                    self.start_time = min([
                        time.get_ticks() + total_time.get(self.difficulty),
                        self.start_time + time_bonus
                    ])
                elif self.count > self.goal:  # infinite mode: change the goalpost
                    print(f"reached {self.goal}")
                    self.goal += goals.get(self.difficulty)
        else:  # game over menu
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
