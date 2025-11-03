# Board class
from utils import get_position_with_row_col


class Board:
    # Initilize the pieces and their color
    def __init__(self, pieces, color_up):
        self.pieces = pieces
        self.color_up = color_up
    
    # Return the color
    def get_color_up(self):
        return self.color_up

    # Return the pieces on the board
    def get_pieces(self):
        return self.pieces

    # Returns the piece by its index
    def get_piece_by_index(self, index):
        return self.pieces[index]

    def has_piece(self, position):
        string_pos = str(position)
        for piece in self.pieces:
            if piece.get_position() == string_pos:
                return True
        return False

    # Returns the row number
    def get_row_number(self, position):
        return position // 4

    # Returns the column number
    def get_col_number(self, position):
        remainder = position % 4
        column_position = remainder * 2
        if (self.get_row_number(position)) % 2 == 0:
            return column_position
        return column_position + 1

    # Return row of a piece
    def get_row(self, row_number):
        row_pos = [0, 1, 2, 3]
        row_pos = list(map((lambda pos: str(pos + (4 * row_number))), row_pos))
        row = []

        for piece in self.pieces:
            if piece.get_position() in row_pos:
                row.append(piece)

        return set(row)

    # Returns a piece based on position on the board
    def get_pieces_by_coords(self, *coords):
        row_memory = dict()
        results = []

        for coord in coords:
            if coord[0] in row_memory:
                row = row_memory[coord[0]]
            else:
                row = self.get_row(coord[0])
                row_memory[coord[0]] = row

            for piece in row:
                if self.get_col_number(int(piece.get_position())) == coord[1]:
                    results.append(piece)
                    break
            else:
                results.append(None)
        return results

    # Moves the pieces on the board
    def move_piece(self, move_index, new_pos):
        def is_eat_movement(pos):
            return abs(self.get_row_number(pos) - self.get_row_number(new_pos)) != 1
    
        # Force the player to eat opponent piece
        def get_eaten_index(pos):
            coords = [self.get_row_number(pos), self.get_col_number(pos)]
            new_coords = [self.get_row_number(new_pos), self.get_col_number(new_pos)]
            eat_coords = [coords[0], coords[1]]

            eat_coords[0] += (new_coords[0] - coords[0]) // 2
            eat_coords[1] += (new_coords[1] - coords[1]) // 2

            eaten_pos = str(get_position_with_row_col(eat_coords[0], eat_coords[1]))

            for index, piece in enumerate(self.pieces):
                if piece.get_position() == eaten_pos:
                    return index
    
        # Allow King pieces to move backwards
        def is_king_movement(piece):
            if piece.is_king():
                return False

            row = self.get_row_number(new_pos)
            color = piece.get_color()
            if self.color_up == color:
                king_row = 0
            else:
                king_row = 7

            return row == king_row

        piece_to_move = self.pieces[move_index]

        # Eats a piece and removes it from the board
        if is_eat_movement(int(piece_to_move.get_position())):
            self.pieces.pop(get_eaten_index(int(piece_to_move.get_position())))
            piece_to_move.set_has_eaten(True)
        else:
            piece_to_move.set_has_eaten(False)

        if is_king_movement(piece_to_move):
            piece_to_move.set_is_king(True)

        piece_to_move.set_position(new_pos)

    # Returns winner once all pieces are eaten
    def get_winner(self):
        color = self.pieces[0].get_color()
        for piece in self.pieces:
            if piece.get_color() != color:
                break
        else:
            return color
        return None