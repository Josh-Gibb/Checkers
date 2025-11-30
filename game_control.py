from piece import Piece
from board import Board
from board_gui import BoardGUI
from held_piece import HeldPiece
from utils import get_surface_mouse_offset, get_position_with_row_col


class GameControl:
    # Initilize the game controls
    def __init__(self, player_color):
        self.turn = player_color
        self.board = None
        self.board_draw = None
        self.held_piece = None
        self.winner = None

        self.setup()

    # Return current turn
    def get_turn(self):
        return self.turn

    # Default setup of the game
    def setup(self):
        # Initial setup
        pieces = []

        for opponent_piece in range(0, 12):
            pieces.append(Piece(str(opponent_piece) + 'BN'))

        for player_piece in range(20, 32):
            pieces.append(Piece(str(player_piece) + 'WN'))

        self.board = Board(pieces, self.turn)
        self.board_draw = BoardGUI(self.board)

    # Display pieces and board on the screen
    def draw_screen(self, display_surface):
        self.board_draw.draw_board(display_surface)
        self.board_draw.draw_pieces(display_surface)

        if self.held_piece is not None:
            self.held_piece.draw_piece(display_surface)

    # Return a winner 
    def get_winner(self):
        return self.winner

    # Ensure that that prioirty is given to eating, and the player is clicking their pieces
    def hold_piece(self, mouse_pos):
        piece_clicked = self.board_draw.get_piece_on_mouse(mouse_pos)
        board_pieces = self.board.get_pieces()
        eat_constraint = False

        if piece_clicked is None:
            return
        if piece_clicked['piece']['color'] != self.turn:
            return

        # Is there any capturing move available for the current color?
        for piece in board_pieces:
            if piece.get_color() != self.turn:
                continue
            for move in piece.get_moves(self.board):
                if move.get('eats_piece'):
                    eat_constraint = True
                    break
            if eat_constraint:
                break

        piece_moves = board_pieces[piece_clicked['index']].get_moves(self.board)

        if eat_constraint:
            piece_moves = list(filter(lambda m: m.get("eats_piece") is True, piece_moves))

        move_spots = []
        for move in piece_moves:
            target_pos = int(move["position"])  # board index 0..31
            row = self.board.get_row_number(target_pos)
            column = self.board.get_col_number(target_pos)
            move_spots.append((row, column))

        self.board_draw.set_move_marks(move_spots)
        self.board_draw.hide_piece(piece_clicked['index'])
        self.set_held_piece(piece_clicked['index'], board_pieces[piece_clicked['index']], mouse_pos)

    # Once the piece is released update board and game
    def release_piece(self):
        if self.held_piece is None:
            return

        position_released = self.held_piece.check_collision(self.board_draw.get_move_marks())
        moved_index = self.board_draw.show_piece()
        piece_moved = self.board.get_piece_by_index(moved_index)

        if position_released is not None:
            self.board.move_piece(moved_index, self.board_draw.get_position_by_rect(position_released))
            self.board_draw.set_pieces(self.board_draw.get_piece_properties(self.board))
            self.winner = self.board.get_winner()

            jump_moves = list(filter(lambda move: move["eats_piece"] == True, piece_moved.get_moves(self.board)))

            if len(jump_moves) == 0 or piece_moved.get_has_eaten() == False:
                self.turn = "B" if self.turn == "W" else "W"

        self.held_piece = None
        self.board_draw.set_move_marks([])

    # Ensuring the piece select is set on a new and valid tile
    def set_held_piece(self, index, piece, mouse_pos):
        surface = self.board_draw.get_surface(piece)
        offset = get_surface_mouse_offset(self.board_draw.get_piece_by_index(index)["rect"], mouse_pos)
        self.held_piece = HeldPiece(surface, offset)
