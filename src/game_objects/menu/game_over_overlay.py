from pygame import Surface, SRCALPHA, event, QUIT, mouse, SYSTEM_CURSOR_HAND, SYSTEM_CURSOR_ARROW

from src.game_objects.menu.button import Button
from src.settings import windows_height, windows_width, overlay_background_color

RESET = event.custom_type()


class GameOverOverlay:
    def __init__(self):
        self.surface = Surface((windows_width, windows_height), SRCALPHA)
        self.surface.fill(overlay_background_color)

        # Create buttons
        restart_button = Button("assets/restart_button.png", callback=lambda: event.post(event.Event(RESET)))
        restart_button.pos.top = windows_height / 2 - restart_button.image.get_rect().height
        exit_button = Button("assets/exit_button.png", callback=lambda: event.post(event.Event(QUIT)))
        exit_button.pos.top = windows_height / 2 + exit_button.image.get_rect().height
        self.buttons = [restart_button, exit_button]

        # Draw buttons
        for button in self.buttons:
            button.pos.centerx = windows_width / 2  # center horizontally
            self.surface.blit(button.image, button.pos)

    def click(self, pos: [int, int]):
        """Transmits the click to the appropriate button"""
        for button in self.buttons:
            if button.is_in(pos):
                button.click()
                return

    def on_mouse_motion(self, pos: [int, int]):
        """Checks if the cursor is over a button"""
        is_clickable = False
        for button in self.buttons:
            if button.is_in(pos):
                is_clickable = True
                break
        if is_clickable:
            mouse.set_cursor(SYSTEM_CURSOR_HAND)
        else:
            mouse.set_cursor(SYSTEM_CURSOR_ARROW)
