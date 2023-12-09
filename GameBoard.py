# from pygame import Vector2
# from enum import Enum
import pygame


class GameBoard:
    # class SquareFlag(Enum):
    #     EMPTY = 0
    #     CIRCLE = 1
    #     CROSS = 2
    def __init__(self) -> None:
        self._board_size = 6
        self._board = []
        self._cell_size = 96
        self._end_of_game = False
        self._board_render_margin = (42, 42)
        self._cell_spacing = 12
        self._winner = "None"

    def set_up_board(self) -> None:
        for y in range(self._board_size):
            for x in range(self._board_size):
                self._board.append(0)

    def calculate_cell_index(self, mouse_position: (int, int)) -> (bool, int):
        index_x = (mouse_position[0] - self._board_render_margin[0])//(self._cell_size + self._cell_spacing)
        if index_x < 0 or index_x > self._board_size - 1:
            return False, 0
        if mouse_position[0] - self._board_render_margin[0] > (index_x+1) * (self._cell_size + self._cell_spacing) - self._cell_spacing:
            return False, 0

        index_y = (mouse_position[1] - self._board_render_margin[1])//(self._cell_size + self._cell_spacing)
        if index_y < 0 or index_y > self._board_size - 1:
            return False, 0
        if mouse_position[1] - self._board_render_margin[1] > (index_y+1) * (self._cell_size + self._cell_spacing) - self._cell_spacing:
            return False, 0

        cell_index = index_x + index_y * self._board_size

        return True, cell_index

    def update(self, cell_index: int, symbol: str) -> bool:
        if cell_index < 0 or cell_index > self._board_size**2 - 1:
            return False
        if self._board[cell_index] != 0:
            return False

        if symbol == "cross":
            self._board[cell_index] = 2
        else:
            self._board[cell_index] = 1
        # if self._bot._check_winning():
        #     pass
        if self._check_winning():
            print("GG")
        return True

    def _check_winning(self) -> bool:
        # checking columns:
        for y in range(self._board_size):
            array = []
            for x in range(self._board_size):
                array.append(self._board[y*self._board_size+x])
            if self._check_array(array)[0]:
                return True
        # checking rows:
        for x in range(self._board_size):
            array = []
            for y in range(self._board_size):
                array.append(self._board[y*self._board_size+x])
            if self._check_array(array)[0]:
                return True
        # checking diagonals:
        array = [self._board[i] for i in range(0, 36, 7)]
        if self._check_array(array)[0]:
            return True
        array = [self._board[i] for i in range(1, 30, 7)]
        if self._check_array(array)[0]:
            return True
        array = [self._board[i] for i in range(6, 35, 7)]
        if self._check_array(array)[0]:
            return True
        array = [self._board[i] for i in range(4, 25, 5)]
        if self._check_array(array)[0]:
            return True
        array = [self._board[i] for i in range(5, 31, 5)]
        if self._check_array(array)[0]:
            return True
        array = [self._board[i] for i in range(11, 32, 5)]
        if self._check_array(array)[0]:
            return True
        return False
# check array and winning logic in bot?

    def _check_array(self, array: []) -> (bool, bool):  # second bool is for checking if array is winable
        arrays = []
        subarray = []
        for index, value in enumerate(array):
            if not subarray:
                subarray.append(value)
            else:
                if value == subarray[0]:
                    subarray.append(value)
                    if index == len(array) - 1:
                        arrays.append(list(subarray))
                else:
                    arrays.append(list(subarray))
                    subarray = []
                    subarray.append(value)

        for arr in arrays:
            if len(arr) == 5 and arr[0] != 0:
                return (True, False)
        return (False, False)

    @property
    def end_of_game(self):
        return self._end_of_game

    def render_board(self, screen) -> None:
        for index, cell in enumerate(self._board):
            start_X = (index % self._board_size) * (self._cell_size + 12) + self._board_render_margin[0]
            start_Y = (index // self._board_size) * (self._cell_size + 12) + self._board_render_margin[0]
            cell_Rect = pygame.Rect(start_X, start_Y, self._cell_size, self._cell_size)
            if cell == 1:
                color = "green"
            elif cell == 2:
                color = "red"
            else:
                color = "white"

            pygame.draw.rect(screen, color, cell_Rect, 0, 10)
            pygame.draw.rect(screen, 'black', cell_Rect, 3, 10)
