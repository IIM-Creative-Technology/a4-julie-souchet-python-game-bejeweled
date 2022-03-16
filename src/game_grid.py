from math import floor
from typing import Optional

from src.game_objects.square.base_square import BaseSquare
from src.game_objects.square.square_factory import SquareFactory
from src.settings import grid_width, grid_height, square_size, minimum_selection
from src.utils.coordinates import from_coord_to_pos, from_pos_to_coord
# type alias
from src.utils.selection import calculate_group

Square = Optional[BaseSquare]


class GameGrid:
    """
    Represents the game's grid,
    with squares that can be either empty (=`None`) or filled
    by a Square.
    The coordinates are independent of the size of the squares in pixels,
    but instead are worth 1 per square.
    You can access a specific square with grid.squares[column][line]
    """

    def __init__(self):
        self.height = floor(grid_height / square_size)
        self.width = floor(grid_width / square_size)
        self.selected_squares: list[Square] = []
        self.squares: list[list[Square]] = []

        # Initializes the grid with random squares
        for x in range(self.width):
            column = []
            for y in range(self.height):
                pos = from_coord_to_pos((x, y))
                column.append(SquareFactory.get_random_item(self, pos))
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

    def reset(self):
        """Fills the whole grid with random squares"""
        for x in range(self.width):
            for y in range(self.height):
                pos = from_coord_to_pos((x, y))
                self.set_square((x, y), SquareFactory.get_random_item(self, pos))

    def fill_first_line(self) -> bool:
        """Loops over the first line and fills in the empty squares.
        Returns a boolean indicating if there was a modification."""
        has_changed = False
        for column in range(self.width):
            if self.squares[column][0] is None:
                pos = from_coord_to_pos((column, 0))
                self.squares[column][0] = SquareFactory.get_random_item(self, pos)
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

    def select(self, coord) -> bool:
        """Select the group of adjacent squares of similar type,
        starting from the given coordinates.
        Returns a boolean indicating if there was a change in selection."""

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
        new_selected = calculate_group(self, coord, current_square.category)
        # print("------- end selection -------")
        self.selected_squares = new_selected
        return True

    def remove_selected(self) -> int:
        """Deletes the selected squares.
        Return how many were deleted."""
        # If there aren't enough selected squares -> ignore
        if self.selected_squares.__len__() < minimum_selection:
            return 0

        for square in self.selected_squares:
            coord = from_pos_to_coord(square.pos)
            self.set_square(coord, None)
        count = self.selected_squares.__len__()
        self.selected_squares.clear()
        return count

    def clear_selection(self):
        """Unselect all selected squares"""
        # If there is no selection -> ignore
        if self.selected_squares.__len__() == 0:
            return

        for square in self.selected_squares:
            square.is_selected = False
        self.selected_squares.clear()
