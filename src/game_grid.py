from math import floor

from assets.settings import grid_width, grid_height, square_size
from src.game_object.game_object_factory import GameObjectFactory


class GameGrid:
    """Represents the game's grid,
    with squares that can be either empty or filled
    by a GameObject"""

    def __init__(self):
        self.height = floor(grid_height / square_size)
        self.width = floor(grid_width / square_size)

        # Init an empty grid
        self.squares = []
        for i in range(self.width):
            column = []
            for j in range(self.height):
                column.append(None)
            self.squares.append(column)

    def fill_first_line(self):
        """Loops over the first line and fills in the empty squares.
        Returns True if there was a modification."""
        has_changed = False
        for column in range(self.width):
            if self.squares[column][0] is None:
                pos = (column * square_size, 0)
                self.squares[column][0] = GameObjectFactory.get_random_item(pos)
                has_changed = True
        return has_changed
