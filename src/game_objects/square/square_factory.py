from random import randint

types = [
    "RedSquare",
    "GreenSquare",
    "YellowSquare"
]


class SquareFactory:
    @staticmethod
    def get_random_item(grid, pos=(0, 0), speed=3):
        index = randint(0, types.__len__() - 1)
        object_name = types[index]
        from src.game_objects.square import square
        return getattr(square, object_name)(grid, pos, speed)
