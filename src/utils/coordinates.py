from math import floor

from assets.settings import square_size


def from_pos_to_coord(pos):
    return floor(pos[0] / square_size), floor(pos[1] / square_size)


def from_coord_to_pos(coord):
    return coord[0] * square_size, coord[1] * square_size
