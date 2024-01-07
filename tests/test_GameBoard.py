import pytest
from GameBoard import GameBoard


def test_board_initialization():
    board = GameBoard()
    board.set_up_board()
    test_board = list()
    for i in range(36):
        test_board.append(0)
    assert board.board == test_board


def test_calculate_cell_index_typical():
    board = GameBoard()
    mouse_position = (45, 45)
    result = board.calculate_cell_index(mouse_position)
    assert result == (True, 0)


def test_calculate_cell_index_x_not_in_cells():
    board = GameBoard()
    mouse_position = (30, 45)
    result = board.calculate_cell_index(mouse_position)
    assert result == (False, 0)


def test_calculate_cell_index_y_not_in_cells():
    board = GameBoard()
    mouse_position = (45, 30)
    result = board.calculate_cell_index(mouse_position)
    assert result == (False, 0)


def test_calculate_cell_index_cell_out_of_board_index_x():
    board = GameBoard()
    mouse_position = (714, 45)
    result = board.calculate_cell_index(mouse_position)
    assert result == (False, 0)


def test_calculate_cell_index_cell_out_of_board_index_y():
    board = GameBoard()
    mouse_position = (45, 714)
    result = board.calculate_cell_index(mouse_position)
    assert result == (False, 0)


def test_update_typical_cross():
    board = GameBoard()
    board.set_up_board()
    result = board.update(2, 'cross')
    assert result is True
    assert board.board[2] == 2


def test_update_typical_circle():
    board = GameBoard()
    board.set_up_board()
    result = board.update(2, 'circle')
    assert result is True
    assert board.board[2] == 1


def test_update_negative_index():
    board = GameBoard()
    board.set_up_board()
    result = board.update(-1, 'cross')
    assert result is False
    assert board.board[2] == 0


def test_update_index_out_of_range():
    board = GameBoard()
    board.set_up_board()
    result = board.update(60, 'cross')
    assert result is False
    assert board.board[2] == 0


def test_update_wrong_symbol():
    board = GameBoard()
    board.set_up_board()
    result = board.update(2, 'test')
    assert result is False
    assert board.board[2] == 0


def test_update_cell_already_taken():
    board = GameBoard()
    board.set_up_board()
    result = board.update(2, 'cross')
    assert result is True
    assert board.board[2] == 2
    result = board.update(2, 'cross')
    assert result is False


def test_undo_moves_typical():
    board = GameBoard()
    board.set_up_board()
    board.update(2, 'cross')
    board.update(1, 'cross')
    board.undo_moves([1, 2])
    assert board.board[1] == 0
    assert board.board[2] == 0


def test_undo_moves_that_were_not_maded():
    board = GameBoard()
    board.set_up_board()
    with pytest.raises(ValueError):
        board.undo_moves([1, 2])


def test_undo_moves_negative_index():
    board = GameBoard()
    board.set_up_board()
    with pytest.raises(IndexError):
        board.undo_moves([-1])


def test_undo_moves_index_out_of_range():
    board = GameBoard()
    board.set_up_board()
    with pytest.raises(IndexError):
        board.undo_moves([60])
