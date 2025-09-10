from utils import get_position_with_row_col

class Piece:
    def __init__(self, name):
        # Example: <position><color><isKing?> 16WN
        self.name = name
        self.has_eaten = False # True if the piece instance has eaten a piece in its last move
    
    def get_name(self):
        return self.name

    def get_position(self):
        return self.name[:-2]

    def get_color(self):
        return self.name[-2]
    
    def get_has_eaten(self):
        return self.has_eaten

    def is_king(self):
        return True if self.name[-1] == 'Y' else False
    
    def set_position(self, new_position):
        # Receives a new position and assigns it.
        # position_index is used because the position part of self.name can be a one or two digit number. 
        position_index = 1 if len(self.name) == 3 else 2
        self.name = str(new_position) + self.name[position_index:]
    
    def set_is_king(self, new_is_king):
        is_king = "Y" if new_is_king else "N"
        self.name = self.name[:-1] + is_king

    def set_has_eaten(self, has_eaten):
        self.has_eaten = has_eaten

    def get_adjacent_squares(self, board):
        # Receives a Board object, returns at max four squares, all of which are potential moves
        current_col = board.get_col_number(int(self.get_position()))
        current_row = board.get_row_number(int(self.get_position()))
        all_coords = []

        if self.is_king():
            all_coords = [(current_row - 1, current_col - 1), (current_row - 1, current_col + 1), (current_row + 1, current_col - 1), (current_row + 1, current_col + 1)]
        else:
            if board.get_color_up() == self.get_color():
                all_coords = [(current_row - 1, current_col - 1), (current_row - 1, current_col + 1)]
            else:
                all_coords = [(current_row + 1, current_col - 1), (current_row + 1, current_col + 1)]
        
        # Because of the offset values above (+1 or -1), it's necessary to check if any invalid coordinates are on the list.
        return list(filter(lambda coords: coords[0] != -1 and coords[0] != 8 and coords[1] != -1 and coords[1] != 8, all_coords))

    def get_moves(self, board):
        # Receives a board, returns all possible moves. For more info check test specifications.
        def get_eat_position(piece, coords):
            # Receives a piece that is obstructing this piece's way and its (row, column) coordinates.
            # Returns the position to move in order to eat the piece, or None if it's impossible.
            if (piece.get_color() == own_color) or (coords[0] in (0, 7)) or (coords[1] in (0, 7)):
                return None

            if coords[1] > current_col:
                # (coords[0] - current_row) returns 1 if the target is below this piece, and -1 otherwise.
                position_to_eat = (coords[0] + (coords[0] - current_row), coords[1] + 1)
            else:
                position_to_eat = (coords[0] + (coords[0] - current_row), coords[1] - 1)
            
            position_num = get_position_with_row_col(position_to_eat[0], position_to_eat[1])
            
            return None if board.has_piece(position_num) else position_num

        current_col = board.get_col_number(int(self.get_position()))
        current_row = board.get_row_number(int(self.get_position()))
        possible_moves = []
        own_color = self.get_color()

        possible_coords = self.get_adjacent_squares(board)

        close_squares = board.get_pieces_by_coords(*possible_coords)
        empty_squares = []

        for index, square in enumerate(close_squares):
            # Empty squares are potential moves. Pieces are potential eating movements.
            if square is None:
                empty_squares.append(index)
            else:
                position_to_eat = get_eat_position(square, possible_coords[index])
                if position_to_eat is None:
                    continue
                
                possible_moves.append({"position": str(position_to_eat), "eats_piece": True})

        if len(possible_moves) == 0:
            # This is skipped if this piece can eat any other, because it is forced to eat it.
            for index in empty_squares:
                new_position = get_position_with_row_col(possible_coords[index][0], possible_coords[index][1])
                possible_moves.append({"position": str(new_position), "eats_piece": False})
        
        return possible_moves