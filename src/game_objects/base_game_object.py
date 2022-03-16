from pygame import image


class BaseGameObject:
    """Represents a game object (square + UI elements)"""

    def __init__(self, image_name: str, pos=(0, 0)):
        self.image = image.load(image_name).convert_alpha()
        self.pos = self.image.get_rect().move(pos)

    def __str__(self):
        return f"<'{self.pos.topleft}>"

    def is_in(self, pos):
        """Returns whether the given point is inside the object"""
        return self.pos.collidepoint(pos)
