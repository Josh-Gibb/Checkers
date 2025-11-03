# Class for each piece 
from utils import get_position_with_row_col

class Piece:
    # Initilize a piece
    def __init__(self, name):
        self.name = name
        self.has_eaten = False
    # Returns piece name, consists of position, color, king status, and hidden
    def get_name(self):
        return self.name

    # Return piece position
    def get_position(self):
        return self.name[:-2]

    # Return piece color
    def get_color(self):
        return self.name[-2]

    # Return whether piece has been eaten
    def get_has_eaten(self):
        return self.has_eaten

    # Return whether a piece is a king or not
    def is_king(self):
        return self.name[-1] == 'Y'

    # Set a new position for a piece
    def set_position(self, new_position):
        position_index = 1 if len(self.name) == 3 else 2
        self.name = str(new_position) + self.name[position_index:]

    # Set a piece to be king
    def set_is_king(self, new_is_king):
        if new_is_king:
            self.name = self.name[:-1] + "Y"
        else:
            self.name = self.name[:-1] + "N"

    # Set a value for if a piece has been eaten
    def set_has_eaten(self, new_has_eaten):
        self.has_eaten = new_has_eaten

    # Get possible moves for a piece
    def get_adjacent_squares(self, board):
        current_col = board.get_col_number(int(self.get_position()))
        current_row = board.get_row_number(int(self.get_position()))

        if self.is_king():
            coords = [
                (current_row - 1, current_col - 1),
                (current_row - 1, current_col + 1),
                (current_row + 1, current_col - 1),
                (current_row + 1, current_col + 1),
            ]
        else:
            if board.get_color_up() == self.get_color():
                coords = [(current_row - 1, current_col - 1),
                          (current_row - 1, current_col + 1)]
            else:
                coords = [(current_row + 1, current_col - 1),
                          (current_row + 1, current_col + 1)]

        return [c for c in coords if c[0] not in (-1, 8) and c[1] not in (-1, 8)]

    # Return all legal moves
    def get_moves(self, board):
        def get_eat_position(blocking_piece, coords):
            if (blocking_piece.get_color() == own_color) or (coords[0] in (0, 7)) or (coords[1] in (0, 7)):
                return None

            if coords[1] > current_col:
                target = (coords[0] + (coords[0] - current_row), coords[1] + 1)
            else:
                target = (coords[0] + (coords[0] - current_row), coords[1] - 1)

            position_num = get_position_with_row_col(target[0], target[1])
            return None if board.has_piece(position_num) else position_num

        current_col = board.get_col_number(int(self.get_position()))
        current_row = board.get_row_number(int(self.get_position()))
        own_color = self.get_color()

        possible_coords = self.get_adjacent_squares(board)
        close_squares = board.get_pieces_by_coords(*possible_coords)

        possible_moves = []
        empty_indices = []

        for idx, occupant in enumerate(close_squares):
            if occupant is None:
                empty_indices.append(idx)
            else:
                eat_pos = get_eat_position(occupant, possible_coords[idx])
                if eat_pos is not None:
                    possible_moves.append({"position": str(eat_pos), "eats_piece": True})

        if len(possible_moves) == 0:
            for idx in empty_indices:
                nr, nc = possible_coords[idx]
                new_pos = get_position_with_row_col(nr, nc)
                possible_moves.append({"position": str(new_pos), "eats_piece": False})

        return possible_moves
