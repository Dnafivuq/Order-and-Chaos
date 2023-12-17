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

    def load_board(self, board: list) -> None:
        self._board = board
        self._indexes_arrays.clear()
        self._load_indexes_to_check()

    def set_difficulty(self, difficulty: str) -> None:
        self._dificulty = difficulty

    def _get_board_values_array(self, indexes_array: list) -> list:
        board_values_array = [self._board[i] for i in indexes_array]
        return board_values_array

    def _load_indexes_to_check(self) -> None:
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
        def create_array_info(max: str, symbol: int, array: list) -> dict:
            return {'symbol': symbol, 'symbol_count': max, 'indexes_array': array}

        arrays_closest_to_win = []

        for indexes_array in self._indexes_arrays:  # finding array(s) closest to win 
            board_values_array = self._get_board_values_array(indexes_array)
            symbol_count = self._amount_of_each_symbol_in_array(board_values_array)

            if symbol_count['cross'] >= symbol_count['circle']:
                array_info = create_array_info(symbol_count['cross'], 'cross', indexes_array)
            else:
                array_info = create_array_info(symbol_count['circle'], 'circle', indexes_array)

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
            print(array_info['symbol'])
            picked_symbol = symbol_dict[_return_oposite_symbol(array_info['symbol'])]
            indexes_array = array_info['indexes_array']
            board_values_array = self._get_board_values_array(indexes_array)
            for index, cell_value in enumerate(board_values_array):
                # print(f'\n\t {self._board[indexes_array[index]]}')  # debugin
                if cell_value == 0:
                    board_values_array[index] = picked_symbol
                    if not self._check_array_winnability(board_values_array):
                        return (indexes_array[index], symbol_dict[picked_symbol])
                    board_values_array[index] = 0  # set cell value back to 0
            picked_symbol = symbol_dict[array_info['symbol']]
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
                return (indexes_array[index], symbol_dict[picked_symbol])
            board_values_array[index] = picked_symbol  # convert symbol str to int
            if self._check_array_win(board_values_array):
                picked_symbol = symbol_dict[_return_oposite_symbol(array_info['symbol'])]
            return (indexes_array[index], symbol_dict[picked_symbol])  # convert symbol int to str

    def _pick_opitmal_cell_order(self) -> (int, str):
        # starting move is always (14, circle) or make it random?
        if 0 == 1:  # first move
            return (14, "circle")
        arrays_closest_to_win = self._find_arrays_closest_to_win()
        pass

    def _pick_random_cell(self) -> int:
        available_cells = [index for index, cell in enumerate(self._board) if cell == 0]
        print(f'move options: {available_cells}')
        if len(available_cells) == 0:
            raise ValueError('no available cells')
        symbol = 'cross'
        if random.randint(0, 1) == 0:
            symbol = 'circle'
        return (available_cells[random.randrange(0, len(available_cells))], symbol)

    def check_winning(self) -> str:  # keep it as check winning, but split some of it to 'update arrays', that only returns true if one of them is won, so array winnability can be better used in undoing moves.
        # if update_arrays():   return 'order'
        # if len(self._indexes_arrays):  return 'chaos'
        # return ''
        # check_array can be renamed to update arrays or something like that
        temporary_indexes_arrays = []
        print('\t<====>')
        for indexes_array in self._indexes_arrays:
            array = self._get_board_values_array(indexes_array)
            print(array)
            result = self._check_array(array)
            if result[0] is True:
                return "order"
            if result[1] is True:
                temporary_indexes_arrays.append(indexes_array)
                print('added')
            else:  # else added only for debuging purposes
                print('deleted')
        self._indexes_arrays = temporary_indexes_arrays
        if len(self._indexes_arrays) == 0:
            return "chaos"
        return ""

    def make_move(self, role: str) -> (int, str):
        if self._dificulty == "easy":
            return self._pick_random_cell()
        elif self._dificulty == "difficult":
            if role == "chaos":
                return self._pick_optimal_cell_chaos()
            elif role == "order":
                return self._pick_opitmal_cell_order()
        return Exception("No move made")

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

    def _check_array(self, array: list) -> (bool, bool):  # second bool is for checking if array is winable
        if self._check_array_win(array):
            return (True, True)  # second True in this case is just a gap filler.
        winnability = self._check_array_winnability(array)
        return (False, winnability)
