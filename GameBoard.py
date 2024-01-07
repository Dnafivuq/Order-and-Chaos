import pygame


class GameBoard:
    """
    A class representing the game board.

    ...

    Attributes
    ----------
    BOARD_SIZE: int
        The board size (constant = 6)
    board: list
        List storing the board info:
            > EMPTY = 0
            > CIRCLE = 1
            > CROSS = 2
    CELL_SIZE: int
        The board cell size
    BOARD_RENDER_MARGIN: tuple[int, int]
        The starting point of board rendering
    CELL_SPACING: int
        The gap between two board cells
    cross_img: pygame.Surface
        The cross symbol image for rendering
    circle_img: pygame.Surface
        The circle symbol image for rendering

    Methods
    -------
    load_symbols_texture(cross_path: str, circle_path: str)
        Loads images for cross and cicle symbols.
    set_up_board()
        Resets the board.
    board()
        Returns the board list.
    calculate_cell_index(mouse_position: tuple[int, int])
        Calculates the board cell that contains mouse position.
    update(cell_index: int, symbol: str)
        Updates the board cell by given index to a given symbol.
    undo_moves(moves: list[int])
        Undoes the given moves.
    render(screen: pygame.Surface)
        Rendering the board to a surface.
    """

    def __init__(self) -> None:
        self._BOARD_SIZE = 6
        self._board = []
        self._CELL_SIZE = 96
        self._BOARD_RENDER_MARGIN = (42, 42)
        self._CELL_SPACING = 12
        self._cross_img = None
        self._circle_img = None

    def load_symbols_texture(self, cross_path: str, circle_path: str) -> None:
        """
        Loads images for cross and cicle symbols.
        Automatically scales images to fit into board cells.
        Function does not handle wrong image paths.

        Raises
        ------
        FileNotFoundError
            If no image is found by given path.

        Parameters
        ----------
        cross_path: str
            Path to the cross image
        circle_path: str
            Path to the circle image
        """

        self._cross_img = pygame.image.load(cross_path)
        self._circle_img = pygame.image.load(circle_path)
        cross_img_factor = self._CELL_SIZE / self._cross_img.get_size()[0]
        circle_img_factor = self._CELL_SIZE / self._circle_img.get_size()[0]
        self._cross_img = pygame.transform.scale_by(self._cross_img, cross_img_factor)
        self._circle_img = pygame.transform.scale_by(self._circle_img, circle_img_factor)

    def set_up_board(self) -> None:
        """
        Resets the board - sets the list values to zeros.
        """

        self._board.clear()
        for _ in range(self._BOARD_SIZE**2):
            self._board.append(0)

    @property
    def board(self) -> list[int]:
        """
        Returns
        -------
        List[int]
            The board values.
        """

        return self._board

    def calculate_cell_index(self, mouse_position: tuple[int, int]) -> tuple[bool, int]:
        """
        Calculates the board cell that contains mouse position.

        Parameters
        ----------
        mouse_position: tuple[int, int]
            The mouse position

        Returns
        -------
        (bool, int)
            > True if one of board cell contains mouse position
            > Index of calculated cell
        """

        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        index_x = (mouse_x - self._BOARD_RENDER_MARGIN[0])//(self._CELL_SIZE + self._CELL_SPACING)
        if index_x < 0 or index_x > self._BOARD_SIZE - 1:
            return False, 0
        if mouse_x - self._BOARD_RENDER_MARGIN[0] > (index_x+1) * (self._CELL_SIZE + self._CELL_SPACING) - self._CELL_SPACING:
            return False, 0

        index_y = (mouse_y - self._BOARD_RENDER_MARGIN[1])//(self._CELL_SIZE + self._CELL_SPACING)
        if index_y < 0 or index_y > self._BOARD_SIZE - 1:
            return False, 0
        if mouse_y - self._BOARD_RENDER_MARGIN[1] > (index_y+1) * (self._CELL_SIZE + self._CELL_SPACING) - self._CELL_SPACING:
            return False, 0

        cell_index = index_x + index_y * self._BOARD_SIZE

        return True, cell_index

    def update(self, cell_index: int, symbol: str) -> bool:
        """
        Updates the board cell by given index to a given symbol.

        Parameters
        ----------
        cell_index: int
            Index of a cell
        symbol: str
            Symbol that the cell will be set to
        """

        if cell_index < 0 or cell_index > self._BOARD_SIZE**2 - 1:  # index out of range
            return False
        if self._board[cell_index] != 0:  # cell is already cross or circle
            return False

        if symbol == "cross":
            self._board[cell_index] = 2
        elif symbol == "circle":
            self._board[cell_index] = 1
        else:
            return False
        return True

    def undo_moves(self, moves: list[int]) -> None:
        """
        Undoes the given moves.

        Raises
        ------
        IndexError
            If move index is incorrect
        ValueError
            If move was not done yet

        Parameters
        ----------
        moves: list[int]
            List of moves to undo
        """

        for move_index in moves:
            if move_index < 0 or move_index >= self._BOARD_SIZE**2:
                raise IndexError
            if self._board[move_index] == 0:
                raise ValueError
            self._board[move_index] = 0

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the board to given surface.

        Parameters
        ----------
        screen: pygame.Surface
            Surface that the board will be rendered to
        """

        for index, cell in enumerate(self._board):
            start_X = (index % self._BOARD_SIZE) * (self._CELL_SIZE + 12) + self._BOARD_RENDER_MARGIN[0]
            start_Y = (index // self._BOARD_SIZE) * (self._CELL_SIZE + 12) + self._BOARD_RENDER_MARGIN[0]
            cell_Rect = pygame.Rect(start_X, start_Y, self._CELL_SIZE, self._CELL_SIZE)

            background_color = pygame.Color(204, 255, 255)
            pygame.draw.rect(screen, background_color, cell_Rect, 0, 10)
            pygame.draw.rect(screen, pygame.Color(26, 26, 26), cell_Rect, 3, 10)
            if cell == 1:
                screen.blit(self._circle_img, (start_X, start_Y))
            elif cell == 2:
                screen.blit(self._cross_img, (start_X, start_Y))
