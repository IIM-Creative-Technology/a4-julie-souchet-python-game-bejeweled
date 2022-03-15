from pygame import image

from src.utils.coordinates import from_pos_to_coord


class BaseGameObject:
    """Represents a game object"""

    def __init__(self, image_name: str, grid, pos=(0, 0), speed=3):
        self.speed = speed
        self.image = image.load(image_name).convert_alpha()
        self.pos = self.image.get_rect().move(pos)
        self.grid = grid
        self.category = None
        self.is_selected = False
        self.is_moving = False

    def __str__(self):
        return f"<'{self.category}', {self.pos.topleft}, selected={self.is_selected}, moving={self.is_moving}>"

    def move(self):
        """Checks if the object can move, and if possible, do it.
        Return true if the object has moved, or false otherwise."""
        if self.can_move():
            self.is_moving = True
            # Move
            prev_coord = from_pos_to_coord(self.pos)
            self.pos = self.pos.move(0, self.speed)
            new_coord = from_pos_to_coord(self.pos)
            # Crossed a square -> update grid
            if new_coord != prev_coord:
                self.grid.move_square(prev_coord, new_coord)

        else:
            self.is_moving = False

        return not self.is_moving

    def can_move(self):
        """Returns whether the object can move down"""
        coord = from_pos_to_coord(self.pos)
        return self.grid.is_free_below(coord)

    def is_in(self, pos):
        """Returns whether the given point is inside the object"""
        return self.pos.collidepoint(pos)
