from utils import get_piece_gui_coords, get_piece_position
import pygame

# Preload images
BLACK_PIECE_SURFACE = pygame.image.load("images/black_piece.png")
WHITE_PIECE_SURFACE = pygame.image.load("images/white_piece.png")
BOARD = pygame.image.load("images/board.png")
BLACK_KING_PIECE_SURFACE = pygame.image.load("images/black_king_piece.png")
WHITE_KING_PIECE_SURFACE = pygame.image.load("images/white_king_piece.png")
MOVE_MARK = pygame.image.load("images/marking.png")

BOARD_POSITION = (26, 26)
TOPLEFTBORDER = (34, 34)
SQUARE_DIST = 56

# Class for the Board GUI
class BoardGUI:
    # Initilize the pieces, board, and move marks
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

            piece_properties["rect"] = pygame.Rect(
                get_piece_gui_coords((piece_row, piece_column), SQUARE_DIST, TOPLEFTBORDER), (41, 41))
            piece_properties["color"] = piece.get_color()
            piece_properties["is_king"] = piece.is_king()
            pieces.append(piece_properties)
        return pieces

    # Returns a piece by its index
    def get_piece_by_index(self, index):
        return self.pieces[index]

    # Return if a piece must be hidden
    def hide_piece(self, index):
        self.hidden_piece = index
 
    def show_piece(self):
        piece_shown = self.hidden_piece
        self.hidden_piece = -1
        return piece_shown

    # Draw Pieces on the board
    def draw_pieces(self, display_surface):
        for index, piece in enumerate(self.pieces):
            if index == self.hidden_piece:
                continue
            if piece['is_king']:
                display_surface.blit(BLACK_KING_PIECE_SURFACE if piece["color"] == "B" else WHITE_KING_PIECE_SURFACE,
                                     piece["rect"])
            else:
                display_surface.blit(BLACK_PIECE_SURFACE if piece["color"] == "B" else WHITE_PIECE_SURFACE,
                                     piece["rect"])

    # Draw Board
    def draw_board(self, display_surface):
        display_surface.blit(BOARD, BOARD_POSITION)

        if (len(self.move_marks) != 0):
            for rect in self.move_marks:
                display_surface.blit(MOVE_MARK, rect)

    # Return the png of a piece, dependent on the ID of the piece
    def get_surface(self, piece):
        surfaces = [BLACK_PIECE_SURFACE, WHITE_PIECE_SURFACE, BLACK_KING_PIECE_SURFACE, WHITE_KING_PIECE_SURFACE]
        if piece.is_king():
            surfaces = surfaces[2:]
        else:
            surfaces = surfaces[:2]
        if piece.get_color() == 'B':
            return surfaces[0]
        else:
            return surfaces[1]

    # To make the piece follow the mouse when rect
    def get_position_by_rect(self, rect):
        return get_piece_position((rect.x, rect.y), SQUARE_DIST, TOPLEFTBORDER)

    # Returns an array containing possible moves of a piece
    def get_move_marks(self):
        return self.move_marks

    # Display potential move marks on the GUI
    def set_move_marks(self, pos_list):
        if len(pos_list) == 0:
            self.move_marks = []
            return
        self.move_marks = []
        for row, column in pos_list:
            self.move_marks.append(
                pygame.Rect(
                    get_piece_gui_coords((row, column), SQUARE_DIST, TOPLEFTBORDER),
                    (44, 44) 
                )
            )

    # Select the piece which the mouse is interacting with
    def get_piece_on_mouse(self, mouse_pos):
        for index, piece in enumerate(self.pieces):
            if piece["rect"].collidepoint(mouse_pos):
                return {"index": index, "piece": piece}
        return None
