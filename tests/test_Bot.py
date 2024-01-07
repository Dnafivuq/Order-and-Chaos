from Bot import Bot
from GameBoard import GameBoard
import pytest


def test_bot_initialization():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    assert bot._board == board.board
    assert len(bot._indexes_arrays) != 0
    assert bot._first_move is True


def test_set_difficulty_easy():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    assert bot._dificulty == "hard"
    bot.set_difficulty("easy")
    assert bot._dificulty == "easy"


def test_set_difficulty_hard():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    assert bot._dificulty == "hard"
    bot.set_difficulty("easy")
    assert bot._dificulty == "easy"
    bot.set_difficulty("hard")
    assert bot._dificulty == "hard"


def test_set_difficulty_incorrect_difficulty():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    with pytest.raises(ValueError):
        bot.set_difficulty("test")


def test_check_winning_no_winner():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    result = bot.check_winning()
    assert result == ""


def test_check_winning_order():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(5):
        board._board[i] = 1
    bot.load_board(board.board)
    result = bot.check_winning()
    assert result == "order"


def test_check_winning_chaos():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(36):
        if i % 2 == 0:
            board._board[i] = 1
        else:
            board._board[i] = 2
    bot.load_board(board.board)
    result = bot.check_winning()
    assert result == "chaos"


def test_make_move_order_easy_difficulty():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(35):
        board._board[i] = 1
    bot.load_board(board.board)
    bot.set_difficulty("easy")
    result = bot.make_move("order")
    assert result[0] == 35
    assert result[1] == "cross" or result[1] == "circle"


def test_make_move_chaos_easy_difficulty():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(35):
        board._board[i] = 1
    bot.load_board(board.board)
    bot.set_difficulty("easy")
    bot._first_move = False
    result = bot.make_move("chaos")
    assert result[0] == 35
    assert result[1] == "cross" or result[1] == "circle"


def test_make_move_order_hard_difficulty():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._first_move = False
    bot.set_difficulty("hard")
    result = bot.make_move("order")
    assert result[0] == 4
    assert result[1] == "circle"


def test_make_move_chaos_hard_difficulty():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._first_move = False
    bot.set_difficulty("hard")
    result = bot.make_move("chaos")
    assert result[0] == 4
    assert result[1] == "cross"


def test_get_board_values_array():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    bot.load_board(board.board)
    result = bot._get_board_values_array([0, 1, 3, 9, 10])
    assert result == [1, 1, 1, 0, 0]


def test_get_board_values_array_index_out_of_range():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    with pytest.raises(IndexError):
        bot._get_board_values_array([60])


def test_load_indexes_to_check():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    bot.load_board(board.board)
    bot._load_indexes_to_check()
    indexes = [
        [0, 1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10, 11],
        [12, 13, 14, 15, 16, 17],
        [18, 19, 20, 21, 22, 23],
        [24, 25, 26, 27, 28, 29],
        [30, 31, 32, 33, 34, 35],
        [0, 6, 12, 18, 24, 30],
        [1, 7, 13, 19, 25, 31],
        [2, 8, 14, 20, 26, 32],
        [3, 9, 15, 21, 27, 33],
        [4, 10, 16, 22, 28, 34],
        [5, 11, 17, 23, 29, 35],
        [0, 7, 14, 21, 28, 35],
        [1, 8, 15, 22, 29],
        [6, 13, 20, 27, 34],
        [4, 9, 14, 19, 24],
        [5, 10, 15, 20, 25, 30],
        [11, 16, 21, 26, 31]
        ]
    assert bot._indexes_arrays == indexes


def test_find_arrays_closest_to_win_one_array():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    bot.load_board(board.board)
    result = bot._find_arrays_closest_to_win()
    assert len(result) == 1
    assert result[0]['symbol'] == 'circle'
    assert result[0]['symbol_count'] == 4
    assert result[0]['indexes_array'] == [0, 1, 2, 3, 4, 5]


def test_find_arrays_closest_to_win_multiple_arrays():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    for i in range(6, 10):
        board._board[i] = 2
    bot.load_board(board.board)
    result = bot._find_arrays_closest_to_win()
    assert len(result) == 2
    assert result[0]['symbol'] == 'circle'
    assert result[0]['symbol_count'] == 4
    assert result[0]['indexes_array'] == [0, 1, 2, 3, 4, 5]
    assert result[1]['symbol'] == 'cross'
    assert result[1]['symbol_count'] == 4
    assert result[1]['indexes_array'] == [6, 7, 8, 9, 10, 11]


def test_pick_optimal_cell_chaos_block_row_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 4
    assert result[1] == "cross"


def test_pick_optimal_cell_chaos_block_row_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 2
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 4
    assert result[1] == "circle"


def test_pick_optimal_cell_chaos_block_row_case_3():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(12, 15):
        board._board[i] = 2
    board.board[13] = 0
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 13
    assert result[1] == "circle"


def test_pick_optimal_cell_chaos_block_column_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(0, 19, 6):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 24
    assert result[1] == "cross"


def test_pick_optimal_cell_chaos_block_column_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(0, 19, 6):
        board._board[i] = 1
    board._board[6] = 0
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 6
    assert result[1] == "cross"


def test_pick_optimal_cell_chaos_block_column_case_3():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    board._board[0] = 1
    board._board[5] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 30
    assert result[1] == "circle"


def test_pick_optimal_cell_chaos_block_diagonal_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(5, 21, 5):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 25
    assert result[1] == "cross"


def test_pick_optimal_cell_chaos_block_diagonal_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(11, 30, 5):
        board._board[i] = 2
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 31
    assert result[1] == "circle"


def test_pick_optimal_cell_chaos_block_diagonal_case_3():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(6, 33, 7):
        board._board[i] = 2
    bot.load_board(board.board)
    bot._update_arrays()
    result = bot._pick_optimal_cell_chaos()
    assert result[0] == 34
    assert result[1] == "circle"


def test_pick_optimal_cell_order_row_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] == 4
    assert result[1] == "circle"


def test_pick_optimal_cell_order_row_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(4):
        board._board[i] = 2
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] == 4
    assert result[1] == "cross"


def test_pick_optimal_cell_order_row_case_3():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(12, 15):
        board._board[i] = 2
    board.board[13] = 0
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] in (13, 15, 16)
    assert result[1] == "cross"


def test_pick_optimal_cell_order_column_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(0, 19, 6):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] == 24
    assert result[1] == "circle"


def test_pick_optimal_cell_order_column_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(0, 19, 6):
        board._board[i] = 1
    board._board[6] = 0
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] in (6, 24)
    assert result[1] == "circle"


def test_pick_optimal_cell_order_column_case_3():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    board._board[0] = 1
    board._board[5] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] in (6, 12, 18, 24)
    assert result[1] == "circle"


def test_pick_optimal_cell_order_diagonal_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(5, 21, 5):
        board._board[i] = 1
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] == 25
    assert result[1] == "circle"


def test_pick_optimal_cell_order_diagonal_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(11, 30, 5):
        board._board[i] = 2
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] == 31
    assert result[1] == "cross"


def test_pick_optimal_cell_order_diagonal_case_3():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(6, 33, 7):
        board._board[i] = 2
    bot.load_board(board.board)
    bot._update_arrays()
    bot._first_move = False
    result = bot._pick_optimal_cell_order()
    assert result[0] == 34
    assert result[1] == "cross"


def test_amount_of_each_symbol_in_array():
    bot = Bot()
    result = bot._amount_of_each_symbol_in_array([0, 1, 2, 1, 0])
    assert result['circle'] == 2
    assert result['cross'] == 1


def test_amount_of_each_symbol_in_array_empty():
    bot = Bot()
    result = bot._amount_of_each_symbol_in_array([0, 0, 0, 0, 0])
    assert result['circle'] == 0
    assert result['cross'] == 0


def test_amount_of_each_symbol_in_array_incorrect_values():
    bot = Bot()
    with pytest.raises(ValueError):
        bot._amount_of_each_symbol_in_array([0, -1, 0, 0, 0])


def test_split_array_into_subarrays_case_1():
    bot = Bot()
    result = bot._split_array_into_subarrays([0, 0, 0, 1])
    assert len(result) == 2
    assert result[0] == [0, 0, 0]
    assert result[1] == [1]


def test_split_array_into_subarrays_case_2():
    bot = Bot()
    result = bot._split_array_into_subarrays([0, 0, 2, 0, 1])
    assert len(result) == 4
    assert result[0] == [0, 0]
    assert result[1] == [2]
    assert result[2] == [0]
    assert result[3] == [1]


def test_split_array_into_subarrays_case_3():
    bot = Bot()
    result = bot._split_array_into_subarrays([1, 1, 2, 0, 1, 1, 0])
    assert len(result) == 5
    assert result[0] == [1, 1]
    assert result[1] == [2]
    assert result[2] == [0]
    assert result[3] == [1, 1]
    assert result[4] == [0]


def test_split_array_into_subarrays_array_of_leght_one():
    bot = Bot()
    result = bot._split_array_into_subarrays([0])
    assert len(result) == 1
    assert result[0] == [0]


def test_split_array_into_subarrays_array_full_of_one_symbol():
    bot = Bot()
    result = bot._split_array_into_subarrays([0, 0, 0, 0])
    assert len(result) == 1
    assert result[0] == [0, 0, 0, 0]


def test_split_array_into_subarrays_empty_array():
    bot = Bot()
    with pytest.raises(ValueError):
        bot._split_array_into_subarrays([])


def test_check_array_win_case_1():
    bot = Bot()
    array = [1, 1, 2, 0, 0, 0]
    result = bot._check_array_win(array)
    assert result is False


def test_check_array_win_case_2():
    bot = Bot()
    array = [1, 1, 1, 0, 0]
    result = bot._check_array_win(array)
    assert result is False


def test_check_array_win_case_3():
    bot = Bot()
    array = [1, 0, 0, 0, 0, 0]
    result = bot._check_array_win(array)
    assert result is False


def test_check_array_win_case_4():
    bot = Bot()
    array = [1, 1, 1, 1, 1]
    result = bot._check_array_win(array)
    assert result is True


def test_check_array_win_case_5():
    bot = Bot()
    array = [2, 2, 2, 2, 2, 0]
    result = bot._check_array_win(array)
    assert result is True


def test_check_array_winnability_case_1():
    bot = Bot()
    array = [1, 1, 2, 0, 0, 0]
    result = bot._check_array_winnability(array)
    assert result is False


def test_check_array_winnability_case_2():
    bot = Bot()
    array = [1, 1, 1, 0, 0]
    result = bot._check_array_winnability(array)
    assert result is True


def test_check_array_winnability_case_3():
    bot = Bot()
    array = [1, 0, 0, 0, 0, 0]
    result = bot._check_array_winnability(array)
    assert result is True


def test_check_array_winnability_case_4():
    bot = Bot()
    array = [1, 1, 1, 1, 1]
    result = bot._check_array_winnability(array)
    assert result is True


def test_check_array_winnability_case_5():
    bot = Bot()
    array = [1, 0, 0, 0, 0, 1]
    result = bot._check_array_winnability(array)
    assert result is False


def test_check_array_winnability_case_6():
    bot = Bot()
    array = [1, 0, 0, 0, 1]
    result = bot._check_array_winnability(array)
    assert result is True


def test_check_array_winnability_case_7():
    bot = Bot()
    array = [1, 0, 2, 0, 0]
    result = bot._check_array_winnability(array)
    assert result is False


def test_check_array_winnability_case_8():
    bot = Bot()
    array = [1, 2, 0, 0, 0, 2]
    result = bot._check_array_winnability(array)
    assert result is True


def test_check_array_winnability_case_9():
    bot = Bot()
    array = [0, 0, 0, 0, 0, 0]
    result = bot._check_array_winnability(array)
    assert result is True


def test_check_array_winnability_case_10():
    bot = Bot()
    array = [0, 0, 0, 0, 0]
    result = bot._check_array_winnability(array)
    assert result is True


def test_update_arrays_case_1():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(0, 5):
        board._board[i] = 2
    bot.load_board(board.board)
    result = bot._update_arrays()
    assert result is True


def test_update_arrays_case_2():
    bot = Bot()
    board = GameBoard()
    board.set_up_board()
    for i in range(36):
        if i % 2 == 0:
            board._board[i] = 1
        else:
            board._board[i] = 2
    bot.load_board(board.board)
    result = bot._update_arrays()
    assert result is False
    assert len(bot._indexes_arrays) == 0
