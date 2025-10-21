from piece import Piece
from board import Board
from board_gui import BoardGUI

# Game control file
class GameControl:
    def __init__(self, player_color):
        self.turn = player_color
        self.board = None
        self.board_draw = None
        self.held_piece = None

        self.setup()

    # Finds the users turn
    def get_turn(self):
        return self.turn

    # The default board setup
    def setup(self):
        # Initial setup
        pieces = []

        for opponent_piece in range(0, 12):
            pieces.append(Piece(str(opponent_piece) + 'BN'))

        for player_piece in range(20, 32):
            pieces.append(Piece(str(player_piece) + 'WN'))

        self.board = Board(pieces, self.turn)
        self.board_draw = BoardGUI(self.board)
        pass

    # Draws board and pieces
    def draw_screen(self, display_surface):
        self.board_draw.draw_board(display_surface)
        self.board_draw.draw_pieces(display_surface)

        if self.held_piece is not None:
            self.held_piece.draw_piece(display_surface)

