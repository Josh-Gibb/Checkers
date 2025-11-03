# Returns the position with column
def get_position_with_row_col(row, column):
    return (row * 4) + (column // 2)

# Returns a pieces position
def get_piece_position(coords, square_dist, top_left_coords):
    x_offset = top_left_coords[0]
    y_offset = top_left_coords[1]

    piece_column = (coords[0] - x_offset) // square_dist
    piece_row = (coords[1] - y_offset) // square_dist

    return get_position_with_row_col(piece_row, piece_column)


# Returns the pieces position on the GUI interface
def get_piece_gui_coords(coords, square_dist, top_left_coords):
    horizontal_distance = square_dist * 2
    vertical_distance = square_dist
    piece_row = coords[0]
    piece_column = coords[1]

    x_pos = top_left_coords[0] + (horizontal_distance * (piece_column // 2))
    x_pos = x_pos if piece_row % 2 == 0 else x_pos + vertical_distance
    y_pos = top_left_coords[1] + (vertical_distance * piece_row)

    return (x_pos, y_pos)

# Returns the position on the GUI where a mouse clicked
def get_surface_mouse_offset(surface_pos, mouse_pos):
    return (surface_pos[0] - mouse_pos[0], surface_pos[1] - mouse_pos[1])