from pygame import event, QUIT

from src.game_objects.menu.button import Button
from src.game_objects.menu.overlay import Overlay
from src.settings import windows_width
from src.utils import custom_events


class StartOverlay(Overlay):
    def __init__(self):
        # Create buttons
        buttons = []

        easy_button = Button(
            f"assets/buttons/easy_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_EASY))
        )
        easy_button.pos.top = 20 + (easy_button.image.get_rect().height + 10)
        buttons.append(easy_button)

        medium_button = Button(
            f"assets/buttons/medium_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_MEDIUM))
        )
        medium_button.pos.top = easy_button.pos.bottom + 5
        buttons.append(medium_button)

        hard_button = Button(
            f"assets/buttons/hard_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_HARD))
        )
        hard_button.pos.top = medium_button.pos.bottom + 5
        buttons.append(hard_button)

        infinite_button = Button(
            "assets/buttons/infinite_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_INFINITE))
        )
        infinite_button.pos.top = hard_button.pos.bottom + 20
        buttons.append(infinite_button)

        exit_button = Button(
            "assets/buttons/exit_button.png",
            callback=lambda: event.post(event.Event(QUIT))
        )
        exit_button.pos.top = infinite_button.pos.bottom + 20
        buttons.append(exit_button)

        super().__init__(buttons)

        # Title
        title = self.font.render("Pyjeweled", True, "white")
        rect = title.get_rect()
        pos = (
            (windows_width - rect.width) / 2,
            5
        )
        self.surface.blit(title, pos)
