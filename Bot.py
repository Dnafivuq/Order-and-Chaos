import random


symbol_dict = {
    1: 'circle',
    2: 'cross',
    'circle': 1,
    'cross': 2
    }


class Bot:
    def __init__(self) -> None:
        self._board = []
        self._board_size = 6
        self._dificulty = "difficult"
        self._indexes_arrays = []
        self._first_move = True

    def load_board(self, board: list) -> None:
        self._board = board
        self._load_indexes_to_check()
        self._first_move = True

    def set_difficulty(self, difficulty: str) -> None:
        self._dificulty = difficulty

    def check_winning(self) -> str:
        if self._update_arrays():
            return "order"
        if len(self._indexes_arrays) == 0:
            return "chaos"
        return ""  # no winner yet

    def make_move(self, role: str) -> (int, str):
        if self._dificulty == "easy":
            return self._pick_random_cell()
        elif self._dificulty == "difficult":
            if role == "chaos":
                return self._pick_optimal_cell_chaos()
            elif role == "order":
                return self._pick_opitmal_cell_order()
        return Exception("No move made")

    def undo_moves(self):
        self._load_indexes_to_check()
        self._update_arrays()

    def _get_board_values_array(self, indexes_array: list) -> list:
        board_values_array = [self._board[i] for i in indexes_array]
        return board_values_array

    def _load_indexes_to_check(self) -> None:
        self._indexes_arrays.clear()
        # checking columns:
        for y in range(self._board_size):
            array = []
            for x in range(self._board_size):
                array.append(y * self._board_size + x)
            self._indexes_arrays.append(array)
        # checking rows:
        for x in range(self._board_size):
            array = []
            for y in range(self._board_size):
                array.append(y * self._board_size + x)
            self._indexes_arrays.append(array)

        # checking diagonals:
        array = [i for i in range(0, 36, 7)]
        self._indexes_arrays.append(array)
        array = [i for i in range(1, 30, 7)]
        self._indexes_arrays.append(array)
        array = [i for i in range(6, 35, 7)]
        self._indexes_arrays.append(array)
        array = [i for i in range(4, 25, 5)]
        self._indexes_arrays.append(array)
        array = [i for i in range(5, 31, 5)]
        self._indexes_arrays.append(array)
        array = [i for i in range(11, 32, 5)]
        self._indexes_arrays.append(array)

    def _find_arrays_closest_to_win(self) -> list:
        def create_array_info(symbol: str, symbol_count: int, indexes_array: list) -> dict:
            return {'symbol': symbol, 'symbol_count': symbol_count, 'indexes_array': indexes_array}

        arrays_closest_to_win = []

        for indexes_array in self._indexes_arrays:  # finding array(s) closest to win
            board_values_array = self._get_board_values_array(indexes_array)
            symbol_count = self._amount_of_each_symbol_in_array(board_values_array)

            if symbol_count['cross'] >= symbol_count['circle']:
                array_info = create_array_info('cross', symbol_count['cross'], indexes_array)
            else:
                array_info = create_array_info('circle', symbol_count['circle'], indexes_array)

            if arrays_closest_to_win:
                current_max_symbol_count = arrays_closest_to_win[0]['symbol_count']
                if array_info['symbol_count'] > current_max_symbol_count:
                    arrays_closest_to_win.clear()
                if array_info['symbol_count'] >= current_max_symbol_count:
                    arrays_closest_to_win.append(array_info)
            else:
                arrays_closest_to_win.append(array_info)
        return arrays_closest_to_win

    def _pick_optimal_cell_chaos(self) -> (int, str):
        def _return_oposite_symbol(symbol: str) -> str:
            if symbol == "cross":
                return "circle"
            return "cross"

        arrays_closest_to_win = self._find_arrays_closest_to_win()

        if len(arrays_closest_to_win) == 0:
            raise Exception('No arrays to choose from')
        # else:
        for array_info in arrays_closest_to_win:
            str_picked_symbol = _return_oposite_symbol(array_info['symbol'])
            int_picked_symbol = symbol_dict[str_picked_symbol]
            indexes_array = array_info['indexes_array']
            board_values_array = self._get_board_values_array(indexes_array)
            available_indexes = [index for index, cell_value in enumerate(board_values_array) if cell_value == 0]
            for index in available_indexes:
                board_values_array[index] = int_picked_symbol
                if not self._check_array_winnability(board_values_array):
                    return (indexes_array[index], str_picked_symbol)
                board_values_array[index] = 0  # set cell value back to 0
            str_picked_symbol = array_info['symbol']
            int_picked_symbol = symbol_dict[str_picked_symbol]
            if board_values_array[0] == 0:  # special case, when array winnability depends on first and last square
                index = 0
            elif board_values_array[-1] == 0:
                index = -1
            else:
                # special case: only first and last squares arent 0 and they are not the same (1, 2)
                # so making any move between <1, 4> index doesn't make an array unwinnable
                # thus resulting in executing this lines of code
                # bot can make a random move in this array -> player will make his move
                # -> bot makes the array unwinnable
                index = random.randrange(1, 4)
                return (indexes_array[index], str_picked_symbol)
            board_values_array[index] = int_picked_symbol
            if self._check_array_win(board_values_array):
                str_picked_symbol = _return_oposite_symbol(str_picked_symbol)
            return (indexes_array[index], str_picked_symbol)

    def _pick_opitmal_cell_order(self) -> (int, str):
        # starting move is random for more game diversity
        if self._first_move:
            self._first_move = False
            return self._pick_random_cell()
        arrays_closest_to_win = self._find_arrays_closest_to_win()
        # always try to fill 'mid' squares first, then the 'outsiders'
        for array_info in arrays_closest_to_win:
            indexes_array = array_info['indexes_array']
            picked_symbol = array_info['symbol']
            board_values_array = self._get_board_values_array(indexes_array)
            available_indexes = [index for index, cell in enumerate(board_values_array) if cell == 0]
            print(f'possible indexes: {available_indexes}, in {indexes_array} as {board_values_array}')
            available_middle_indexes = []
            for index in available_indexes:
                if index >= 1 and index <= 4:
                    available_middle_indexes.append(index)
            if available_middle_indexes:
                index = available_middle_indexes[random.randrange(0, len(available_middle_indexes))]
                return (indexes_array[index], picked_symbol)

            index = available_indexes[random.randint(-1, 0)]
            return (indexes_array[index], picked_symbol)

    def _pick_random_cell(self) -> int:
        available_cells = [index for index, cell in enumerate(self._board) if cell == 0]
        if len(available_cells) == 0:
            raise ValueError('no available cells')
        symbol = 'cross'
        if random.randint(0, 1) == 0:
            symbol = 'circle'
        return (available_cells[random.randrange(0, len(available_cells))], symbol)

    def _amount_of_each_symbol_in_array(self, array) -> dict:
        symbol_count = {'circle': 0, 'cross': 0}
        for value in array:
            if value == 1:
                symbol_count['circle'] += 1
            if value == 2:
                symbol_count['cross'] += 1
        return symbol_count

    def _split_array_into_subarrays(self, array: list) -> list:
        array_of_subarrays = []
        subarray = []

        for cell_index, cell_value in enumerate(array):
            if not subarray:
                subarray.append(cell_value)
            else:
                if cell_value == subarray[0]:
                    subarray.append(cell_value)
                    if cell_index == len(array) - 1:  # end of array, add last subarray to list fo arrays
                        array_of_subarrays.append(list(subarray))
                else:
                    array_of_subarrays.append(list(subarray))
                    subarray = []
                    subarray.append(cell_value)
        return array_of_subarrays

    def _check_array_win(self, array: list) -> bool:
        # check for winning:
        array_of_subarrays = self._split_array_into_subarrays(array)
        for subarray in array_of_subarrays:
            if len(subarray) == 5 and subarray[0] != 0:
                return True

    def _check_array_winnability(self, array: list) -> bool:
        # check if array is winnable
        if len(array) == 6:
            if array[0] == array[-1] and array[0] != 0:  # first and last square is the same
                return False
            symbol_count = self._amount_of_each_symbol_in_array(array[1:5])
            if symbol_count['circle'] >= 1 and symbol_count['cross'] >= 1:
                return False
        elif len(array) == 5:  # one of four small (only 5 squares) diagonal arrays - special cases for winnablity
            symbol_count = self._amount_of_each_symbol_in_array(array)
            if symbol_count['circle'] >= 1 and symbol_count['cross'] >= 1:
                return False
        return True

    def _update_arrays(self) -> bool:
        temporary_indexes_arrays = []
        print('#\t<===new update===>')
        for indexes_array in self._indexes_arrays:
            board_values_array = self._get_board_values_array(indexes_array)
            print(board_values_array)
            if self._check_array_win(board_values_array):
                # if array is a winning one, no need for further check - end of the game
                return True
            if self._check_array_winnability(board_values_array):
                temporary_indexes_arrays.append(indexes_array)
                print('added')
            else:  # else added only for debuging purposes
                print('deleted')
        self._indexes_arrays = temporary_indexes_arrays
        return False
