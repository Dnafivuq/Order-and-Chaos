# from pygame import Vector2
# from enum import Enum
import pygame
from Bot import Bot


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
        self._bot = Bot()

    def set_up_board(self) -> None:
        self._board.clear()
        for y in range(self._board_size):
            for x in range(self._board_size):
                self._board.append(0)

    @property
    def board(self) -> []:
        return self._board

    def calculate_cell_index(self, mouse_position: (int, int)) -> (bool, int):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        # change self._board_render_margin to just board_render_margin in order to shorten the lines?
        index_x = (mouse_x - self._board_render_margin[0])//(self._cell_size + self._cell_spacing)
        if index_x < 0 or index_x > self._board_size - 1:
            return False, 0
        if mouse_x - self._board_render_margin[0] > (index_x+1) * (self._cell_size + self._cell_spacing) - self._cell_spacing:
            return False, 0

        index_y = (mouse_y - self._board_render_margin[1])//(self._cell_size + self._cell_spacing)
        if index_y < 0 or index_y > self._board_size - 1:
            return False, 0
        if mouse_y - self._board_render_margin[1] > (index_y+1) * (self._cell_size + self._cell_spacing) - self._cell_spacing:
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
        return True

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
