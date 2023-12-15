import random


class Bot:
    def __init__(self) -> None:
        self._board = []
        self._board_size = 6
        self._dificulty = "easy"
        self._indexes_arrays = []

    def load_board(self, board: list) -> None:
        self._board = board
        self._indexes_arrays = []
        self._load_indexes_to_check()

    def set_difficulty(self, difficulty: str) -> None:
        self._dificulty = difficulty

    def make_move(self, role: str) -> (int, str):
        if self._dificulty == "easy":
            return self._pick_random_cell()
        elif self._dificulty == "difficult":
            if role == "chaos":
                return self._pick_optimal_cell()

    def _pick_optimal_cell(self) -> (int, str):
        def create_array_info(max, symbol, array):
            return {'symbol': symbol, 'symbol_count': max, 'indexes_array': array}

        array_options = []
        for indexes_array in self._indexes_arrays:  # finding the closest to win array(s)
            array = self._get_board_values_array(indexes_array)  # player move -> check winning to delete unwinnable arrays -> make bot do the move
            symbol_count = self._amount_of_each_symbol_in_array(array)

            if symbol_count['cross'] >= symbol_count['circle']:
                array_info = create_array_info(symbol_count['cross'], 'cross', indexes_array)
            else:
                array_info = create_array_info(symbol_count['circle'], 'circle', indexes_array)
            if array_options:
                current_max_symbol_count = array_options[0]['symbol_count']
                if array_info['symbol_count'] > current_max_symbol_count:
                    array_options.clear()
                if array_info['symbol_count'] >= current_max_symbol_count:
                    array_options.append(array_info)
            else:
                array_options.append(array_info)
        if len(array_options) == 0:
            raise Exception('No arrays to choose from')
        else:
            for array_info in array_options:
                print(array_info)

    def _pick_random_cell(self) -> int:
        available_cells = [index for index, cell in enumerate(self._board) if cell == 0]
        print(f'move options: {available_cells}')
        if len(available_cells) == 0:
            raise ValueError('no available cells')
        symbol = 'cross'
        if random.randint(0, 1) == 0:
            symbol = 'circle'
        return (available_cells[random.randrange(0, len(available_cells))], symbol)

    def _get_board_values_array(self, indexes_array):
        board_values_array = [self._board[i] for i in indexes_array]
        return board_values_array

    def check_winning(self) -> str:
        temporary_indexes_arrays = []
        for indexes_array in self._indexes_arrays:
            array = self._get_board_values_array(indexes_array)
            print(array)
            result = self._check_array(array)
            if result[1] is True:
                temporary_indexes_arrays.append(indexes_array)
                print('added')
            if result[0] is True:
                print('win')
                return "order"
        self._indexes_arrays = temporary_indexes_arrays
        if len(self._indexes_arrays) == 0:
            return "chaos"
        return ""

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

    def _amount_of_each_symbol_in_array(self, array) -> dict:
        symbol_count = {'circle': 0, 'cross': 0}
        for value in array:
            if value == 1:
                symbol_count['circle'] += 1
            if value == 2:
                symbol_count['cross'] += 1
        return symbol_count

    def _check_array(self, array: []) -> (bool, bool):  # second bool is for checking if array is winable
        array_of_subarrays = []
        subarray = []

        for cell_index, cell_value in enumerate(array):
            if not subarray:
                subarray.append(cell_value)
            else:
                if cell_value == subarray[0]:
                    subarray.append(cell_value)
                    if cell_index == len(array) - 1:  # end of array, add subarray to list fo arrays
                        array_of_subarrays.append(list(subarray))
                else:
                    array_of_subarrays.append(list(subarray))
                    subarray = []
                    subarray.append(cell_value)
        # check for winning:
        for subarray in array_of_subarrays:
            if len(subarray) == 5 and subarray[0] != 0:
                return (True, True)  # second True in this case is just a gap filler.
        # check if array is stil winnable
        if len(array) == 6:
            if array[0] == array[-1] and array[0] != 0:  # first and last square is the same
                return (False, False)
            symbol_count = self._amount_of_each_symbol_in_array(array[1:5])
            if symbol_count['circle'] >= 1 and symbol_count['cross'] >= 1:
                return (False, False)
        elif len(array) == 5:  # one of four small (only 5 squares) diagonal - special cases for winnablity
            symbol_count = self._amount_of_each_symbol_in_array(array)
            if symbol_count['circle'] >= 1 and symbol_count['cross'] >= 1:
                return (False, False)

        # deafult return value - array is not a winning one (no 5 of one type),
        # but still can be won (possibility for 5 of one type)
        return (False, True)
