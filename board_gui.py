from utils import get_piece_gui_coords
import pygame

# Preload images
BLACK_PIECE_SURFACE = pygame.image.load("images/black_piece.png")
WHITE_PIECE_SURFACE = pygame.image.load("images/white_piece.png")
BOARD = pygame.image.load("images/board.png")

# GUI specifications
BOARD_POSITION = (26, 26)
TOPLEFTBORDER = (34, 34)
SQUARE_DIST = 56

# Board gui class
class BoardGUI:
    def __init__(self, board):
        self.pieces = self.get_piece_properties(board)
        self.hidden_piece = -1
        self.move_marks = []

    def set_pieces(self, piece_list):
        self.pieces = piece_list

    # Creates a dictionary tracking every piece
    def get_piece_properties(self, board):
        initial_pieces = board.get_pieces()
        pieces = []

        for piece in initial_pieces:
            piece_position = int(piece.get_position())
            piece_row = board.get_row_number(piece_position)
            piece_column = board.get_col_number(piece_position)
            piece_properties = dict()

            piece_properties["rect"] = pygame.Rect(get_piece_gui_coords((piece_row, piece_column), SQUARE_DIST, TOPLEFTBORDER), (41, 41))
            piece_properties["color"] = piece.get_color()

            pieces.append(piece_properties)

        return pieces

    def get_piece_by_index(self, index):
        return self.pieces[index]

    def hide_piece(self, index):
        self.hidden_piece = index

    # Shows piece
    def show_piece(self):
        piece_shown = self.hidden_piece
        self.hidden_piece = -1
        return piece_shown

    # Draw Pieces on the board
    def draw_pieces(self, display_surface):
        for index, piece in enumerate(self.pieces):
            if index == self.hidden_piece:
                continue
            display_surface.blit(BLACK_PIECE_SURFACE if piece["color"] == "B" else WHITE_PIECE_SURFACE, piece["rect"])

    # Draw Board
    def draw_board(self, display_surface):
        display_surface.blit(BOARD, BOARD_POSITION)

    def get_surface(self, piece):
        surfaces = [BLACK_PIECE_SURFACE, WHITE_PIECE_SURFACE]
        surfaces = surfaces[:2]
        return surfaces[0] if piece.get_color() == 'B' else surfaces[1]

    def get_position_by_rect(self, rect):
        return get_piece_position((rect.x, rect.y), SQUARE_DIST, TOPLEFTBORDER)

