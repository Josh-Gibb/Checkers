# Board class
class Board:
    def __init__(self, pieces, color_up):
        self.pieces = pieces
        self.color_up = color_up

    def get_color_up(self):
        return self.color_up

    def get_pieces(self):
        return self.pieces

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
        if  (self.get_row_number(position)) % 2 == 0:
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
