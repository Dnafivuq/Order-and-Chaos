import random


class NoEmptyCellsFoundException(Exception):
    "Raised when Bot has no cells to choose from (cannot make a move)"
    pass


class NoArraysFoundException(Exception):
    "Raised when Bot has no arrays to choose from (cannot make a move)"
    pass


# dictionary for symbol converting from str to int and vice versa
symbol_dict = {
    1: 'circle',
    2: 'cross',
    'circle': 1,
    'cross': 2
    }


class Bot:
    """
    A class representing Bot.
    Bot is responsible for making moves and checking if game should end.

    ...

    Attributes
    ----------
    board: list[int]
        Reference to GameBoard board list with symbols
    BOARD_SIZE: int, constant
        One of board's dimension size (board is always square)
    difficulty: str
        Bot difficulty
            > "easy"
            > "hard"
    indexes_arrays: list[list[int]]
        List that hold lists of indexes of board cells for winning checking
    first_move: bool
        Variable needed for bot first move as `order` because the begining move is random

    Methods
    -------
    load_board()
        Loads GameBoard board reference.
    set_difficulty()
        Sets bot difficulty to given.
    check_winning()
        Checks if game should end and return winner.
    make_move()
        Makes bot moves depending on given role and bot difficulty.
    undo_moves()
        Resets bot indexes_array after undoing moves.
    get_board_values_array()
        Gets board values from array of indexes.
    load_indexes_to_check()
        Loads arrays of indexes that needs to be check for game win.
    find_arrays_closest_to_win()
        Returns arrays of indexes closest to winning.
    pick_optimal_cell_chaos()
        Returns optimal chaos move.
    pick_optimal_cell_order()
        Returns optimal order move.
    pick_random_cell()
        Return random move.
    amount_of_each_symbol_in_array()
        Returns number of each symbol in given array.
    split_array_into_subarrays()
        Splits array into arrays based on values.
    check_array_win()
        Checks if array is won.
    check_array_winnability()
        Checks if array is still winnable.
    update_arrays()
        Updates indexes_arrays based on their winnability. Returns True if one of arrays is a winning one.
    """

    def __init__(self) -> None:
        self._board = []
        self._BOARD_SIZE = 6
        self._dificulty = "hard"
        self._indexes_arrays = []
        self._first_move = True

    def load_board(self, board: list[int]) -> None:
        """
        Loads GameBoard board reference for bot moves and winning checking.

        Parameters
        ----------
        board: list[int]
            GameBoard board reference
        """

        self._board = board
        self._load_indexes_to_check()
        self._first_move = True

    def set_difficulty(self, difficulty: str) -> None:
        """
        Sets bot difficulty to given.

        Raises
        ------
        ValueError
            If given difficulty is not "easy" or "hard"

        Parameters
        ----------
        difficulty: str
            Bot difficulty
                > "easy"
                > "hard"
        """

        if difficulty not in ("easy", "hard"):
            raise ValueError
        self._dificulty = difficulty

    def check_winning(self) -> str:
        """
        Checks if game should end and return winner.

        Returns
        -------
        str
            Winner
                > "order"
                > "chaos"
                > "" - if no winner
        """

        if self._update_arrays():
            return "order"
        if len(self._indexes_arrays) == 0:
            return "chaos"
        return ""  # no winner yet

    def make_move(self, role: str) -> tuple[int, str]:
        """
        Makes bot moves depending on given role and bot difficulty.

        Parameters
        ----------
        role: str
            Bot role

        Returns
        -------
        (int, str)
            > Index of GameBoard board cell
            > Bot move symbol
                > "circle"
                > "cross"
        """

        if self._dificulty == "easy":
            return self._pick_random_cell()
        elif self._dificulty == "hard":
            if role == "chaos":
                return self._pick_optimal_cell_chaos()
            elif role == "order":
                return self._pick_optimal_cell_order()

    def undo_moves(self):
        """
        Resets bot indexes_array to deafult.
        Updates indexes_array to current GameBoard state.
        """

        self._load_indexes_to_check()
        self._update_arrays()

    def _get_board_values_array(self, indexes_array: list[list[int]]) -> list[list[int]]:
        """
        Gets GameBoard board cells values based on indexes from array of indexes.

        Parameters
        ----------
        indexes_array: list[list[int]]
            List of lists that contains GameBoard cells indexes for value getting

        Returns
        -------
        list[list[int]]
            List of lists that contains GameBoard cells values
        """

        board_values_array = [self._board[i] for i in indexes_array]
        return board_values_array

    def _load_indexes_to_check(self) -> None:
        """
        Loads arrays of indexes that needs to be check for game win.
        Arrays are lists of columns/rows/diagonal GameBoard cells indexes.
        """

        self._indexes_arrays.clear()
        # checking columns:
        for y in range(self._BOARD_SIZE):
            array = []
            for x in range(self._BOARD_SIZE):
                array.append(y * self._BOARD_SIZE + x)
            self._indexes_arrays.append(array)

        # checking rows:
        for x in range(self._BOARD_SIZE):
            array = []
            for y in range(self._BOARD_SIZE):
                array.append(y * self._BOARD_SIZE + x)
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

    def _find_arrays_closest_to_win(self) -> list[dict]:
        """
        Returns arrays of indexes closest to winning.

        Returns
        -------
        list[dict]
            List of closest to win arrays' info contained in dictionary with keys:
                > "symbol"
                > "symbol_count"
                > "indexes_array"
        """

        def create_array_info(symbol: str, symbol_count: int, indexes_array: list) -> dict:
            return {'symbol': symbol, 'symbol_count': symbol_count, 'indexes_array': indexes_array}

        arrays_closest_to_win = []

        for indexes_array in self._indexes_arrays:
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

    def _pick_optimal_cell_chaos(self) -> tuple[int, str]:
        """
        Returns optimal chaos move.

        Raises
        ------
        NoArraysFoundException
            If there is no array from arrays_closest_to_win to choose from.

        Returns
        -------
        (int, str)
            > Index of GameBoard board cell
            > Bot move symbol
                > "circle"
                > "cross"
        """

        def _return_oposite_symbol(symbol: str) -> str:
            if symbol == "cross":
                return "circle"
            return "cross"

        arrays_closest_to_win = self._find_arrays_closest_to_win()

        if len(arrays_closest_to_win) == 0:
            raise NoArraysFoundException

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

    def _pick_optimal_cell_order(self) -> tuple[int, str]:
        """
        Returns optimal order move.

        Raises
        ------
        NoArraysFoundException
            If there is no array from arrays_closest_to_win to choose from.

        Returns
        -------
        (int, str)
            > Index of GameBoard board cell
            > Bot move symbol
                > "circle"
                > "cross"
        """

        # starting move is random for more game diversity
        if self._first_move:
            self._first_move = False
            return self._pick_random_cell()
        arrays_closest_to_win = self._find_arrays_closest_to_win()
        if len(arrays_closest_to_win) == 0:
            raise NoArraysFoundException
        # always try to fill 'mid' squares first, then the 'outsiders'
        for array_info in arrays_closest_to_win:
            indexes_array = array_info['indexes_array']
            picked_symbol = array_info['symbol']
            board_values_array = self._get_board_values_array(indexes_array)
            available_indexes = [index for index, cell in enumerate(board_values_array) if cell == 0]
            available_middle_indexes = []
            for index in available_indexes:
                if index >= 1 and index <= 4:
                    available_middle_indexes.append(index)
            if available_middle_indexes:
                index = available_middle_indexes[random.randrange(0, len(available_middle_indexes))]
                return (indexes_array[index], picked_symbol)

            index = available_indexes[random.randint(-1, 0)]
            return (indexes_array[index], picked_symbol)

    def _pick_random_cell(self) -> tuple[int, str]:
        """
        Returns random move.

        Raises
        ------
        NoEmptyCellsFoundException
            If there is no empty cells in board to choose from.

        Returns
        -------
        (int, str)
            > Index of GameBoard board cell
            > Bot move symbol
                > "circle"
                > "cross"
        """

        available_cells = [index for index, cell in enumerate(self._board) if cell == 0]
        if len(available_cells) == 0:
            raise NoEmptyCellsFoundException
        symbol = 'cross'
        if random.randint(0, 1) == 0:
            symbol = 'circle'
        return (available_cells[random.randrange(0, len(available_cells))], symbol)

    def _amount_of_each_symbol_in_array(self, array: list[int]) -> dict:
        """
        Returns number of each symbol in given array.

        Raises
        ------
        ValueError
            If array value is not in (0, 1, 2) - incorrect cell value

        Parameters
        ----------
        array: list[int]
            Array to check amount of symbols in it

        Returns
        -------
        dict
            Dictionary with symbol name and it count in array
                > "circle"
                > "cross"
        """

        symbol_count = {'circle': 0, 'cross': 0}
        for value in array:
            if value == 1:
                symbol_count['circle'] += 1
            elif value == 2:
                symbol_count['cross'] += 1
            elif value == 0:
                continue
            else:
                raise ValueError
        return symbol_count

    def _split_array_into_subarrays(self, array: list[int]) -> list[list[int]]:
        """
        Splits array into arrays based on values.
        Splits based on cell values - into longes subarrays of same value
        i.e. [0, 0, 0, 1, 1, 2, 0, 0] -> [[0,0,0], [1,1], [2], [0, 0]]

        Raises
        ------
        ValueError
            If array lenght is equal to zero

        Parameters
        ----------
        array: list[int]
            Array to split into smaller same value arrays

        Returns
        -------
        list[list[int]]
            List of subbarrays of same value
        """

        array_of_subarrays = []
        subarray = []
        if len(array) == 0:
            raise ValueError
        for cell_index, cell_value in enumerate(array):
            if not subarray:
                subarray.append(cell_value)
            else:
                if cell_value == subarray[0]:
                    subarray.append(cell_value)
                else:
                    array_of_subarrays.append(list(subarray))
                    subarray = []
                    subarray.append(cell_value)
            if cell_index == len(array) - 1:  # end of array, add last subarray to list fo arrays
                array_of_subarrays.append(list(subarray))
        return array_of_subarrays

    def _check_array_win(self, array: list[int]) -> bool:
        """
        Checks if array is won.

        Parameters
        ----------
        array: list[int]
            Array to be checked for win

        Returns
        -------
        bool
            True if array is won, else False
        """

        array_of_subarrays = self._split_array_into_subarrays(array)
        for subarray in array_of_subarrays:
            if len(subarray) == 5 and subarray[0] != 0:
                return True
        return False

    def _check_array_winnability(self, array: list[int]) -> bool:
        """
        Checks if array is still winnable.

        Parameters
        ----------
        array: list[int]
            Array to be checked for winnability

        Returns
        -------
        bool
            False if array is not winnable, else True
        """

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
        """
        Updates indexes_arrays based on their winnability. 
        Returns True if one of arrays is a winning one.

        Returns
        -------
        bool
            True if one of arrays is a winning one, else False
        """

        temporary_indexes_arrays = []
        for indexes_array in self._indexes_arrays:
            board_values_array = self._get_board_values_array(indexes_array)
            if self._check_array_win(board_values_array):
                # if array is a winning one, no need for further check - end of the game
                return True
            if self._check_array_winnability(board_values_array):
                temporary_indexes_arrays.append(indexes_array)
        self._indexes_arrays = temporary_indexes_arrays
        return False
