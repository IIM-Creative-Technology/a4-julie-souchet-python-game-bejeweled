from math import floor
from typing import Optional

from assets.settings import grid_width, grid_height, square_size
from src.game_object.base_game_object import BaseGameObject
from src.game_object.game_object_factory import GameObjectFactory
from src.utils.coordinates import from_coord_to_pos

# type alias
Square = Optional[BaseGameObject]


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
        self.selected_squares: list[Square] = []
        self.squares: list[list[Square]] = []

        # Init an empty grid
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
                    string += game_object.category[0]
                string += "|"
            string += "\n------------------------\n"
        return string

    def fill_first_line(self) -> bool:
        """Loops over the first line and fills in the empty squares.
        Returns a boolean indicating if there was a modification."""
        has_changed = False
        for column in range(self.width):
            if self.squares[column][0] is None:
                pos = from_coord_to_pos((column, 0))
                self.squares[column][0] = GameObjectFactory.get_random_item(self, pos)
                has_changed = True
        return has_changed

    def get_square(self, coord) -> Square:
        """Returns the game object present at the given coordinates,
        or None if it's empty or if they are out of bounds."""
        if not (0 <= coord[0] < self.width
                and 0 <= coord[1] < self.height):
            return None
        return self.squares[coord[0]][coord[1]]

    def set_square(self, coord, game_object: Square):
        self.squares[coord[0]][coord[1]] = game_object

    def is_free_below(self, coord) -> bool:
        below = (coord[0], coord[1] + 1)
        return below[1] < self.height and self.get_square(below) is None

    def move_square(self, prev_coord, new_coord):
        game_object = self.get_square(prev_coord)
        self.set_square(prev_coord, None)
        self.set_square(new_coord, game_object)

    def select_square(self, coord) -> bool:
        """Changes the current selected squares.
        Returns a boolean indicating if there was a change."""

        # Check if the current hovered square is already selected
        current_square = self.get_square(coord)
        if current_square is not None and current_square.is_selected:
            return False

        has_changed = False
        # Deselect previous selection
        prev_selected = self.selected_squares
        for square in prev_selected:
            has_changed = True
            square.is_selected = False

        # Select new selection
        if current_square is None or current_square.is_moving:
            return has_changed

        # print("------- start selection -------")
        new_selected = self.get_group(coord, current_square.category)
        # print("------- end selection -------")
        self.selected_squares = new_selected
        return True

    def get_group(self, coord, category):
        """Gets all adjacent (⬆⬇⬅➡) squares of the same category
        with a tree search"""
        # Test current square
        current_square = self.get_square(coord)
        if (current_square is None
                or current_square.is_moving
                or current_square.category != category
                or current_square.is_selected):
            # print("REFUSED", current_square)
            return []
        else:
            current_square.is_selected = True
            square_list = [current_square]
            # print("ACCEPTED", current_square)

        # Expand the search to the current square's neighbors
        candidates = [
            (coord[0] - 1, coord[1]),
            (coord[0] + 1, coord[1]),
            (coord[0], coord[1] - 1),
            (coord[0], coord[1] + 1)
        ]

        for candidate in candidates:
            # Add the result from the search to the list
            found = self.get_group(candidate, category)
            square_list.extend(found)

        # Once search is done, return the updated list
        return square_list
