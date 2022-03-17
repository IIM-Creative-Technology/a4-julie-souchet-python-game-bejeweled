from pygame import Surface, SRCALPHA, mouse, SYSTEM_CURSOR_HAND, SYSTEM_CURSOR_ARROW, font

from src.settings import windows_height, windows_width, overlay_background_color


class Overlay:
    def __init__(self, buttons):
        self.surface = Surface((windows_width, windows_height), SRCALPHA)
        self.surface.fill(overlay_background_color)
        self.buttons = buttons
        self.font = font.Font("assets/fonts/HomemadeApple-Regular.ttf", 56)

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
