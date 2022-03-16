from src.game_objects.square.base_square import BaseSquare


class GreenSquare(BaseSquare):
    def __init__(self, grid, pos=(0, 0), speed=3):
        super().__init__("assets/squares/green.png", grid, pos, speed)
        self.category = "green"


class RedSquare(BaseSquare):
    def __init__(self, grid, pos=(0, 0), speed=3):
        super().__init__("assets/squares/red.png", grid, pos, speed)
        self.category = "red"


class YellowSquare(BaseSquare):
    def __init__(self, grid, pos=(0, 0), speed=3):
        super().__init__("assets/squares/yellow.png", grid, pos, speed)
        self.category = "yellow"
