import random


class Bot:
    def __init__(self) -> None:
        self._board = []
        self._board_size = 6
        self._dificulty = "easy"

    def load_board(self, board: list) -> None:
        self._board = board

    def set_difficulty(self, difficulty: str) -> None:
        self._dificulty = difficulty

    def make_move(self) -> (str, int):
        if self._dificulty == "easy":
            cell_index = self._pick_random_cell()
            if random.randint(0, 1) == 0:
                return cell_index, "cross"
            return cell_index, "circle"
        elif self._dificulty == "difficult":
            pass

    def _pick_random_cell(self) -> int:
        available_cells = [index for index, cell in enumerate(self._board) if cell == 0]
        print(available_cells)
        if len(available_cells) == 0:
            raise ValueError('no available cells')
        return available_cells[random.randrange(0, len(available_cells))]
