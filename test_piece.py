import sys
sys.path.append('..')
from piece import Piece
from board import Board

def test_piece_getters():
    test_piece = Piece('16WN')
    assert test_piece.get_position() == '16'
    assert test_piece.get_color() == 'W'
    assert test_piece.is_king() == False

def test_moves_free():
    # A piece can move freely if there is nothing on the way
    test_piece = Piece('18WN')
    test_board = Board([test_piece], 'W')
    
    assert test_piece.get_moves(test_board) == [{"position": '13', "eats_piece": False}, {"position": '14', "eats_piece": False}]

def test_moves_bounds():
    # A piece cannot move outside of the board
    test_piece = Piece('8WN')
    test_board = Board([test_piece], 'W')

    assert test_piece.get_moves(test_board) == [{"position": '4', "eats_piece": False}]

def test_moves_none():
    # A piece can't eat while getting outside of the board or eat with a piece on the way.
    test_piece = Piece('12WN')
    test_board = Board([test_piece, Piece('8BN'), Piece('9BN'), Piece('5BN')], 'W')
    
    assert test_piece.get_moves(test_board) == []

def test_moves_forced():
    # If a piece can eat another one, it can only do that.
    # Also, it cannot eat a piece of its own color.
    test_piece = Piece('12WN')
    test_board = Board([test_piece, Piece('9BN')], 'W')

    assert test_piece.get_moves(test_board) == [{"position": '5', "eats_piece": True}]
    pass

def test_moves_eat_options():
    # A piece can choose which one to each if given more options.
    test_piece = Piece('13WN')
    test_board = Board([test_piece, Piece('9BN'), Piece('10BN')], 'W')

    assert test_piece.get_moves(test_board) == [{"position": '4', "eats_piece": True}, {"position": '6', "eats_piece": True}]

def test_moves_king():
    # A king can also move backwards.
    test_piece = Piece('4WY')
    test_board = Board([test_piece, Piece('8BN')], 'W')

    assert test_piece.get_moves(test_board) == [{"position": '0', "eats_piece": False}, {"position": '1', "eats_piece": False}, {"position": '9', "eats_piece": False}]