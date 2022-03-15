from pygame import image

from assets.settings import windows_height


class BaseGameObject:
    """Represents a game object"""

    def __init__(self, image_name, pos, speed):
        self.speed = speed
        self.image = image.load(image_name).convert()
        self.pos = self.image.get_rect().move(pos)
        self.type = None

    def move(self):
        """Checks if the object can move, and if possible, do it.
        Return true if the object has moved, or false otherwise."""
        if self.can_move():
            self.pos = self.pos.move(0, self.speed)
            return True
        return False

    def can_move(self):
        return self.pos.bottom < windows_height
