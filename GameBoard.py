import pygame
from Bot import Bot


class GameBoard:
    #     EMPTY = 0
    #     CIRCLE = 1
    #     CROSS = 2

    def __init__(self) -> None:
        self._board_size = 6
        self._board = []
        self._cell_size = 96
        self._board_render_margin = (42, 42)
        self._cell_spacing = 12
        self._bot = Bot()
        self._cross_img = ""
        self._circle_img = ""

    def load_symbols_texture(self, cross_path: str, circle_path: str) -> None:
        self._cross_img = pygame.image.load(cross_path)
        self._circle_img = pygame.image.load(circle_path)
        self._cross_img = pygame.transform.scale_by(self._cross_img, 1.5)
        self._circle_img = pygame.transform.scale_by(self._circle_img, 1.5)

    def set_up_board(self) -> None:
        self._board.clear()
        for _ in range(self._board_size**2):
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
        # change index returning - return index_x, index_y
        # this way correctness of index can be check once - inside the update function

    def update(self, cell_index: int, symbol: str) -> bool:
        if cell_index < 0 or cell_index > self._board_size**2 - 1:  # index out of range
            return False
        if self._board[cell_index] != 0:  # cell is already cross or circle
            return False

        if symbol == "cross":
            self._board[cell_index] = 2
        else:
            self._board[cell_index] = 1
        return True

    def undo_moves(self, moves: list):
        for move_index in moves:
            self._board[move_index] = 0
        
    def render_board(self, screen) -> None:
        for index, cell in enumerate(self._board):
            start_X = (index % self._board_size) * (self._cell_size + 12) + self._board_render_margin[0]
            start_Y = (index // self._board_size) * (self._cell_size + 12) + self._board_render_margin[0]
            cell_Rect = pygame.Rect(start_X, start_Y, self._cell_size, self._cell_size)

            background_color = pygame.Color(204, 255, 255)
            pygame.draw.rect(screen, background_color, cell_Rect, 0, 10)
            pygame.draw.rect(screen, pygame.Color(26, 26, 26), cell_Rect, 3, 10)
            if cell == 1:
                screen.blit(self._circle_img, (start_X, start_Y))
            elif cell == 2:
                screen.blit(self._cross_img, (start_X, start_Y))
