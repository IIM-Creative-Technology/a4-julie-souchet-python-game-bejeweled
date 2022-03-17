from pygame import event, QUIT

from src.game_objects.menu.button import Button
from src.game_objects.menu.overlay import Overlay
from src.settings import windows_height, windows_width
from src.utils.custom_events import RESET


class GameOverOverlay(Overlay):
    def __init__(self, has_won):
        # Create buttons
        restart_button = Button("assets/buttons/restart_button.png", callback=lambda: event.post(event.Event(RESET)))
        restart_button.pos.top = windows_height / 2 - restart_button.image.get_rect().height
        exit_button = Button("assets/buttons/exit_button.png", callback=lambda: event.post(event.Event(QUIT)))
        exit_button.pos.top = windows_height / 2 + exit_button.image.get_rect().height
        buttons = [restart_button, exit_button]
        super().__init__(buttons)

        # Title
        if has_won:
            message = "You win!"
        else:
            message = "You lose ..."
        title = self.font.render(message, True, "white")
        rect = title.get_rect()
        pos = (
            (windows_width - rect.width) / 2,
            50
        )
        self.surface.blit(title, pos)
