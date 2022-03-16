from src.game_objects.base_game_object import BaseGameObject


class Button(BaseGameObject):
    """Clickable element that calls a function"""

    def __init__(self, image_name: str, pos=(0, 0), callback=None):
        super().__init__(image_name, pos)
        self.name = image_name
        self.callback = callback

    def __str__(self):
        return self.name

    def click(self):
        if self.callback is not None:
            self.callback()
