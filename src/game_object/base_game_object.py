from pygame import image

from src.utils.coordinates import from_pos_to_coord


class BaseGameObject:
    """Represents a game object"""

    def __init__(self, image_name, grid, pos=(0, 0), speed=3):
        self.speed = speed
        self.image = image.load(image_name).convert()
        self.pos = self.image.get_rect().move(pos)
        self.grid = grid
        self.type = None

    def move(self):
        """Checks if the object can move, and if possible, do it.
        Return true if the object has moved, or false otherwise."""
        if self.can_move():
            # Move
            prev_pos = self.pos
            prev_coord = from_pos_to_coord(self.pos)
            self.pos = self.pos.move(0, self.speed)
            new_coord = from_pos_to_coord(self.pos)
            # Crossed a square -> update grid
            if new_coord != prev_coord:
                self.grid.move_square(prev_coord, new_coord)

            return True
        return False

    def can_move(self):
        coord = from_pos_to_coord(self.pos)
        return self.grid.is_free_below(coord)
