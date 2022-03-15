from random import randint

types = [
    "RedGameObject",
    "GreenGameObject",
    "YellowGameObject"
]


class GameObjectFactory:
    @staticmethod
    def get_random_item(pos=(0, 0), speed=3):
        index = randint(0, types.__len__() - 1)
        object_name = types[index]
        from src.game_object import game_object
        return getattr(game_object, object_name)(pos, speed)
