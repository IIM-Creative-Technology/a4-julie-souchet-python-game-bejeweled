from src.game_object.base_game_object import BaseGameObject


class GreenGameObject(BaseGameObject):
    def __init__(self, grid, pos=(0, 0), speed=3):
        super().__init__("assets/green.png", grid, pos, speed)
        self.type = "green"


class RedGameObject(BaseGameObject):
    def __init__(self, grid, pos=(0, 0), speed=3):
        super().__init__("assets/red.png", grid, pos, speed)
        self.type = "red"


class YellowGameObject(BaseGameObject):
    def __init__(self, grid, pos=(0, 0), speed=3):
        super().__init__("assets/yellow.png", grid, pos, speed)
        self.type = "yellow"
