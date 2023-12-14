import pygame
from GameBoard import GameBoard
from MouseStructure import Mouse
import GUI
from Bot import Bot


class GameEngine:
    def __init__(self) -> None:
        self._deltaTime = 0
        self._screen = pygame.display.set_mode((960, 720))
        self._running = True
        self._clock = pygame.time.Clock()
        self._board = GameBoard()
        self._board.set_up_board()
        self._selected_symbol = 'circle'
        self._mouse = Mouse()
        self._current_player = "player"
        self._winner = "None"

        self._maked_moves = []

        self._bot = Bot()
        self._bot.load_board(self._board.board)

        self._cross_button = GUI.ChangeSymbolButton("cross")
        self._cross_button.update_position((740, 330))
        self._cross_button.update_size((64, 64))
        self._cross_button.update_colors(("red", "black"))

        self._circle_button = GUI.ChangeSymbolButton("circle")
        self._circle_button.update_position((740+96, 330))
        self._circle_button.update_size((64, 64))
        self._circle_button.update_colors(("green", "yellow"))

    def run(self) -> None:
        self._deltaTime = self._clock.tick(60) / 1000
        while (self._running):
            self._process_events()
            self._update()
            self._render()
        pygame.quit()

    def _process_events(self) -> None:
        self._mouse.reset_mouse_pressing()
        for event in pygame.event.get():
            self._mouse.update_mouse_position(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
                self._mouse._left_button = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 3:  # delete this after testing
                self._mouse._right_button = True

    def _update(self) -> None:
        if self._mouse._right_button:
            print(self._maked_moves)
        if self._current_player == "bot":
            # bot timer - to do
            bot_move = self._bot.make_move()
            if self._board.update(bot_move[0], bot_move[1]):
                self._maked_moves.append(bot_move)
                if self._bot.check_winning():
                    print('bot won')
                self._current_player = "player"
                return
            raise Exception  # only for debuging??
        if self._mouse.left_button_pressing:
            if self._circle_button.check_if_clicked(self._mouse.position):
                self._selected_symbol = self._circle_button.on_click()
                self._cross_button.update_colors(("red", "black"))

            if self._cross_button.check_if_clicked(self._mouse.position):
                self._selected_symbol = self._cross_button.on_click()
                self._circle_button.update_colors(("green", "black"))

            if self._current_player == "player":
                cell_index = self._board.calculate_cell_index(self._mouse.position)
                if not cell_index[0]:  # calculated index is not correct (mouse was outside the game board etc.)
                    return
                if self._board.update(cell_index[1], self._selected_symbol):
                    self._maked_moves.append((cell_index[1], f'p_{self._selected_symbol}'))
                    if self._bot.check_winning():
                        print('player won')
                    self._current_player = "bot"
                    return

    def _render(self) -> None:
        self._screen.fill("grey")
        # pygame.draw.circle(self._screen, "red", pygame.Vector2(600, 400), 40)
        # cell_Rect = pygame.Rect(0, 0, 64, 64)
        self._board.render_board(self._screen)
        self._cross_button.render(self._screen)
        self._circle_button.render(self._screen)

        # pygame.draw.rect(self._screen, "red", cell_Rect)
        pygame.display.flip()
