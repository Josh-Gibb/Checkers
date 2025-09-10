from utils import get_piece_gui_coords, get_piece_position
import pygame

# Preload images
BLACK_PIECE_SURFACE = pygame.image.load("images/black_piece.png")
WHITE_PIECE_SURFACE = pygame.image.load("images/white_piece.png")
BLACK_KING_PIECE_SURFACE = pygame.image.load("images/black_king_piece.png")
WHITE_KING_PIECE_SURFACE = pygame.image.load("images/white_king_piece.png")
MOVE_MARK = pygame.image.load("images/marking.png")
BOARD = pygame.image.load("images/board.png")

# GUI specifications
BOARD_POSITION = (26, 26)
TOPLEFTBORDER = (34, 34)
SQUARE_DIST = 56

class BoardGUI:
    def __init__(self, board):
        self.pieces = self.get_piece_properties(board)
        self.hidden_piece = -1 # This attribute is -1 when no piece must be hidden
        self.move_marks = []

    def set_pieces(self, piece_list):
        self.pieces = piece_list

    def get_piece_properties(self, board):
        # Receives a board object, returns a list of its pieces organized in 3 dictionary keys.
        initial_pieces = board.get_pieces()
        pieces = []

        for piece in initial_pieces:
            piece_position = int(piece.get_position())
            piece_row = board.get_row_number(piece_position)
            piece_column = board.get_col_number(piece_position)
            piece_properties = dict()

            piece_properties["rect"] = pygame.Rect(get_piece_gui_coords((piece_row, piece_column), SQUARE_DIST, TOPLEFTBORDER), (41, 41))
            piece_properties["color"] = piece.get_color()
            piece_properties["is_king"] = piece.is_king()

            pieces.append(piece_properties)
        
        return pieces
    
    def get_piece_by_index(self, index):
        return self.pieces[index]

    def hide_piece(self, index):
        # Index of Board pieces and BoardGUI pieces is kept the same.
        self.hidden_piece = index
    
    def show_piece(self):
        # Reveals hidden piece and returns the piece index
        piece_shown = self.hidden_piece
        self.hidden_piece = -1
        return piece_shown

    def draw_pieces(self, display_surface):
        for index, piece in enumerate(self.pieces):
            if index == self.hidden_piece:
                continue
            
            if piece["is_king"]:
                display_surface.blit(BLACK_KING_PIECE_SURFACE if piece["color"] == "B" else WHITE_KING_PIECE_SURFACE, piece["rect"])
            else:
                display_surface.blit(BLACK_PIECE_SURFACE if piece["color"] == "B" else WHITE_PIECE_SURFACE, piece["rect"])
    
    def draw_board(self, display_surface):
        display_surface.blit(BOARD, BOARD_POSITION)
        
        # Also draws move marks if needed.
        if len(self.move_marks) != 0:
            for rect in self.move_marks:
                display_surface.blit(MOVE_MARK, rect)
    
    def get_piece_on_mouse(self, mouse_pos):
        for index, piece in enumerate(self.pieces):
            if piece["rect"].collidepoint(mouse_pos):
                return {"index": index, "piece": piece}
        
        return None

    def get_surface(self, piece):
        # Returns a proper surface for the given piece.
        surfaces = [BLACK_PIECE_SURFACE, WHITE_PIECE_SURFACE, BLACK_KING_PIECE_SURFACE, WHITE_KING_PIECE_SURFACE]
        surfaces = surfaces[2:] if piece.is_king() else surfaces[:2]

        return surfaces[0] if piece.get_color() == 'B' else surfaces[1]

    def get_move_marks(self):
        return self.move_marks

    def set_move_marks(self, position_list):
        # Sets a list of move marks based on a list of (row, column) tuples.
        if len(position_list) == 0:
            self.move_marks = []

        for position in position_list:
            row = position[0]
            column = position[1]   
            self.move_marks.append(pygame.Rect(get_piece_gui_coords((row, column), SQUARE_DIST, TOPLEFTBORDER), (44, 44)))

    def get_position_by_rect(self, rect):
        # Receives a rect and returns a (row, column) tuple containing the position on the board.
        return get_piece_position((rect.x, rect.y), SQUARE_DIST, TOPLEFTBORDER)
