from pygame import event, QUIT

from src.game_objects.menu.button import Button
from src.game_objects.menu.overlay import Overlay
from src.settings import windows_height
from src.utils import custom_events


class StartOverlay(Overlay):
    def __init__(self):
        buttons = []

        # Create buttons
        easy_button = Button(
            f"assets/buttons/easy_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_EASY))
        )
        easy_button.pos.top = windows_height / 2 - (easy_button.image.get_rect().height + 5) * 3
        buttons.append(easy_button)

        medium_button = Button(
            f"assets/buttons/medium_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_MEDIUM))
        )
        medium_button.pos.top = windows_height / 2 - (medium_button.image.get_rect().height + 5) * 2
        buttons.append(medium_button)

        hard_button = Button(
            f"assets/buttons/hard_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_HARD))
        )
        hard_button.pos.top = windows_height / 2 - (hard_button.image.get_rect().height + 5)
        buttons.append(hard_button)

        infinite = Button(
            "assets/buttons/infinite_button.png",
            callback=lambda: event.post(event.Event(custom_events.START_INFINITE))
        )
        infinite.pos.top = windows_height / 2 + 15
        buttons.append(infinite)

        exit_button = Button(
            "assets/buttons/exit_button.png",
            callback=lambda: event.post(event.Event(QUIT))
        )
        exit_button.pos.top = windows_height / 2 + exit_button.image.get_rect().height + 60
        buttons.append(exit_button)

        buttons_str = [button.__str__() for button in buttons]

        super().__init__(buttons)
