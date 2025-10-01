def get_position_with_row_col(row, column):
    # Receives a piece's row and column positions and returns the (0-31) position on the board.
    # Position is calculated taking into consideration the fact that each leftmost dark square on the board is (row * 4).
    # Other squares are obtained using the column parameter.
    return (row * 4) + (column // 2)

def get_piece_position(coords, square_dist, top_left_coords):
    # Receives a piece's x and y coordinates along with the GUI's specific properties, returning a piece's position (0 - 31) on the board.
    # GUI properties should be a list containing the distance in pixels of each square and the top left corner's coordinates.
    x_offset = top_left_coords[0]
    y_offset = top_left_coords[1]
    
    piece_column = (coords[0] - x_offset) // square_dist
    piece_row = (coords[1] - y_offset) // square_dist

    return get_position_with_row_col(piece_row, piece_column)

def get_piece_gui_coords(coords, square_dist, top_left_coords):
    # Receives a piece's row and column position along with the GUI's specific properties, returning a piece's coordinates on the GUI.
    # Information about the GUI properties can be read on the get_piece_position function.
    horizontal_distance = square_dist * 2
    vertical_distance = square_dist
    piece_row = coords[0]
    piece_column = coords[1]
    
    # Calculating x_pos takes into consideration one square between each possible to move square and a one square offset in odd rows.
    x_pos = top_left_coords[0] + (horizontal_distance * (piece_column // 2))
    x_pos = x_pos if piece_row % 2 == 0 else x_pos + vertical_distance
    y_pos = top_left_coords[1] + (vertical_distance * piece_row)
    
    return (x_pos, y_pos)

def get_surface_mouse_offset(surface_pos, mouse_pos):
    # Receives the position (x, y) of a surface and the mouse. Returns the offset used to determine where the surface was clicked.
    return (surface_pos[0] - mouse_pos[0], surface_pos[1] - mouse_pos[1])