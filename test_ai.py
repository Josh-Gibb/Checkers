import sys
sys.path.append('..')
from piece import Piece
from board import Board
from ai import AI

def test_minimax_maximize():
    # minimax() returns the maximum value possible
    test_ai = AI('B')
    test_board = Board([Piece('9WN'), Piece('17BN'), Piece('21BN')], 'B')
    assert test_ai.minimax(test_board, True, 1, 'B') == 1
    assert test_ai.minimax(test_board, True, 2, 'B') == 1

def test_minimax_minimize():
    # minimax() returns the minimum value possible
    test_ai = AI('B')
    test_board = Board([Piece('9WN'), Piece('17BN'), Piece('21BN')], 'B')
    assert test_ai.minimax(test_board, False, 1, 'B') == 1
    assert test_ai.minimax(test_board, False, 2, 'B') == 0

def test_get_move():
    # get_move() should return the move with the maximum value
    test_ai = AI('B')
    test_board = Board([Piece('9WN'), Piece('17BN'), Piece('21BN')], 'B')
    assert test_ai.get_move(test_board) in [{"position_from": "17", "position_to": "13"}, {"position_from": "21", "position_to": "18"}]