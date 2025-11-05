import sys
sys.path.append('..')
from board import Board
from piece import Piece

def test_has_piece():
    # Simple test to assert has_piece detects a piece on a given position.
    test_board = Board([Piece('12WY'), Piece('26BY'), Piece('8WN')], 'W')
    assert test_board.has_piece(26) == True
    assert test_board.has_piece(10) == False

def test_get_row_number():
    # Asserts if get_row_number correctly returns the row for a given position. The first row is 0.
    # Positions are also zero-indexed.
    test_board = Board([], 'W')
    assert test_board.get_row_number(2) == 0
    assert test_board.get_row_number(3) == 0
    assert test_board.get_row_number(4) == 1

def test_get_col_number():
    # Asserts if get_col_number correctly returns the column for a given position. The first column is 0.
    test_board = Board([], 'B')
    assert test_board.get_col_number(0) == 0
    assert test_board.get_col_number(1) == 2
    assert test_board.get_col_number(4) == 1
    assert test_board.get_col_number(31) == 7

def test_get_row():
    # Checks if a row is properly returned.
    test_white = Piece('4WN')
    test_black = Piece('6BN')
    test_board = Board([test_white, test_black], 'B')
    assert test_board.get_row(1) == {test_white, test_black}

def test_get_pieces_by_coords():
    # This method should receive (row, column) pairs and return the pieces on these coordinates.
    test_piece = Piece('8WN')
    test_board = Board([test_piece], 'W')
    assert test_board.get_pieces_by_coords((2, 0), (3, 0)) == [test_piece, None]