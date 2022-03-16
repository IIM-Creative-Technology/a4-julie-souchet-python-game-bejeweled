def calculate_group(grid, coord, category):
    """Gets all adjacent (⬆⬇⬅➡) squares of the same category
    with a tree search"""
    # Test current square
    current_square = grid.get_square(coord)
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
        found = calculate_group(grid, candidate, category)
        square_list.extend(found)

    # Once search is done, return the updated list
    return square_list
