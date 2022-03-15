from math import floor

from assets.settings import grid_width, grid_height, square_size
from src.game_object.game_object_factory import GameObjectFactory
from src.utils.coordinates import from_coord_to_pos


class GameGrid:
    """
    Represents the game's grid,
    with squares that can be either empty (=`None`) or filled
    by a GameObject.
    The coordinates are independent of the size of the squares in pixels,
    but instead are worth 1 per square.
    You can access a specific square with grid.squares[column][line]
    """

    def __init__(self):
        self.height = floor(grid_height / square_size)
        self.width = floor(grid_width / square_size)
        self.selected_square = None

        # Init an empty grid
        self.squares = []
        for i in range(self.width):
            column = []
            for j in range(self.height):
                column.append(None)
            self.squares.append(column)

    def __str__(self):
        string = "\n------------------------\n"
        for line in range(self.height):
            for column in range(self.width):
                game_object = self.squares[column][line]
                if game_object is None:
                    string += " "
                else:
                    string += game_object.type[0]
                string += "|"
            string += "\n------------------------\n"
        return string

    def fill_first_line(self):
        """Loops over the first line and fills in the empty squares.
        Returns a boolean indicating if there was a modification."""
        has_changed = False
        for column in range(self.width):
            if self.squares[column][0] is None:
                pos = from_coord_to_pos((column, 0))
                self.squares[column][0] = GameObjectFactory.get_random_item(self, pos)
                has_changed = True
        return has_changed

    def get_square(self, coord):
        return self.squares[coord[0]][coord[1]]

    def set_square(self, coord, game_object):
        self.squares[coord[0]][coord[1]] = game_object

    def is_free_below(self, coord):
        below = (coord[0], coord[1] + 1)
        return below[1] < self.height and self.is_free(below)

    def is_free(self, coord):
        return self.get_square(coord) is None

    def move_square(self, prev_coord, new_coord):
        game_object = self.get_square(prev_coord)
        self.set_square(prev_coord, None)
        self.set_square(new_coord, game_object)

    def select_square(self, coord):
        """Changes the current selected square.
        Returns a boolean indicating if there was a change."""
        prev_selected = self.selected_square
        new_selected = self.get_square(coord)
        # No change
        if prev_selected is new_selected:
            return False

        # Switch selected
        if prev_selected is not None:
            prev_selected.is_selected = False
        self.selected_square = new_selected
        if self.selected_square is not None:
            self.selected_square.is_selected = True

        return True
