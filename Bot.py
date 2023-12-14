import random


class Bot:
    def __init__(self) -> None:
        self._board = []
        self._board_size = 6
        self._dificulty = "easy"
        self._indexes_array = []

    def load_board(self, board: list) -> None:
        self._board = board
        self._load_indexes_to_check()

    def set_difficulty(self, difficulty: str) -> None:
        self._dificulty = difficulty

    def make_move(self) -> (int, str):
        if self._dificulty == "easy":
            cell_index = self._pick_random_cell()
            if random.randint(0, 1) == 0:
                return cell_index, "cross"
            return cell_index, "circle"
        elif self._dificulty == "difficult":
            pass

    def _pick_random_cell(self) -> int:
        available_cells = [index for index, cell in enumerate(self._board) if cell == 0]
        print(f'move options: {available_cells}')
        if len(available_cells) == 0:
            raise ValueError('no available cells')
        return available_cells[random.randrange(0, len(available_cells))]

    def _get_board_values_array(self, indexes_array):
        board_values_array = [self._board[i] for i in indexes_array]
        return board_values_array

    def check_winning(self):
        temporary_indexes_array = []
        for indexes_array in self._indexes_array:
            array = self._get_board_values_array(indexes_array)
            print(array)
            result = self._check_array(array)
            if result[1] is True:
                temporary_indexes_array.append(indexes_array)
                print('added')
            if result[0] is True:
                print('win')
                return True
        if len(temporary_indexes_array) == 0:
            return True
        self._indexes_array = temporary_indexes_array
        return False

    def _load_indexes_to_check(self) -> None:
        # checking columns:
        for y in range(self._board_size):
            array = []
            for x in range(self._board_size):
                array.append(y * self._board_size + x)
            self._indexes_array.append(array)
        # checking rows:
        for x in range(self._board_size):
            array = []
            for y in range(self._board_size):
                array.append(y * self._board_size + x)
            self._indexes_array.append(array)

        # checking diagonals:
        array = [i for i in range(0, 36, 7)]
        self._indexes_array.append(array)
        array = [i for i in range(1, 30, 7)]
        self._indexes_array.append(array)
        array = [i for i in range(6, 35, 7)]
        self._indexes_array.append(array)
        array = [i for i in range(4, 25, 5)]
        self._indexes_array.append(array)
        array = [i for i in range(5, 31, 5)]
        self._indexes_array.append(array)
        array = [i for i in range(11, 32, 5)]
        self._indexes_array.append(array)

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
        elif len(array) == 5:  # one of four small (only 5 squares) diagonal - special cases for winnablity
            pass

        # deafult return value - array is not a winning one (no 5 of one type),
        # but still can be won (possibility for 5 of one type)
        return (False, True)
