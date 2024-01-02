import pygame
from GameBoard import GameBoard
from MouseStructure import Mouse
import GUI
from Bot import Bot


class GameEngine:
    def __init__(self) -> None:
        cross_img_path = "./assets/cross_new.png"
        circle_img_path = "./assets/circle_new.png"

        self._delta_time = 0
        self._screen = pygame.display.set_mode((960, 720))
        self._running = True
        self._clock = pygame.time.Clock()
        self._board = GameBoard()
        self._board.load_symbols_texture(cross_img_path, circle_img_path)
        self._mouse = Mouse()

        self._maked_moves = list()

        self._bot = Bot()
        self._bot_difficulty = "difficult"
        self._bot_role = "order"

        self._game_state = "menu"

        self._cross_button = GUI.ChangeSymbolButton("cross")
        self._cross_button.update_position((740, 316))
        self._cross_button.update_size((64, 64))
        self._cross_button.update_colors(("grey", "black"))
        self._cross_button.load_image(cross_img_path)

        self._circle_button = GUI.ChangeSymbolButton("circle")
        self._circle_button.update_position((740+96, 316))
        self._circle_button.update_size((64, 64))
        self._circle_button.update_colors(("grey", "black"))
        self._circle_button.load_image(circle_img_path)

        self._order_button = GUI.Button((64, 64), (740, 120))
        self._chaos_button = GUI.Button((64, 64), (740+96, 120))

        self._undo_button = GUI.Button((164, 50), (740, 430), "light blue", "black")
        self._undo_button.load_image("./assets/undo_button.png")
        self._restart_button = GUI.Button((164, 50), (740, 430+80), "light blue", "black")
        self._restart_button.load_image("./assets/restart_button.png")
        self._menu_button = GUI.Button((164, 50), (740, 430+160), "light blue", "black")
        self._menu_button.load_image("./assets/menu_button.png")

        self._start_button = GUI.Button((164, 50), (398, 600), "light blue", "black")
        self._start_button.load_image("./assets/start_button.png")

    def _start_game(self):
        self._current_role = "order"
        self._selected_symbol = self._circle_button.on_click()
        self._cross_button.update_colors(("", "black"))
        self._winner = ""

        self._game_state = "game"

        self._maked_moves.clear()
        self._mouse.reset_mouse_pressing()

        self._board.set_up_board()

        self._bot.load_board(self._board.board)
        self._bot.set_difficulty(self._bot_difficulty)
        self._bot_role = "chaos"  # temp, delete after testing
        self._bot_time_delay = 1.5  # 1.5s
        self._bot_clock = self._bot_time_delay

        print('<###> Starting Game...\n')

    def run(self) -> None:
        self._delta_time = self._clock.tick(60) / 1000
        self._start_game()
        while (self._running):
            self._process_events()
            if self._game_state == "menu":
                self._menu_update()
                self._menu_render()
            elif self._game_state == "game":
                self._game_update()
                self._game_render()
        # pygame.quit()

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

    def _menu_update(self) -> None:
        if self._mouse.left_button_pressing:
            if self._start_button.check_if_clicked(self._mouse.position):
                self._start_game()
        return

    def _menu_render(self) -> None:
        self._screen.fill(pygame.Color(0, 255, 153))
        self._start_button.render(self._screen)
        pygame.display.flip()

    def _game_update(self) -> None:
        def _return_oposite_role(role: str) -> str:
            if role == "chaos":
                return "order"
            return "chaos"

        if self._current_role == "order":
            self._order_button.on_click()
            self._chaos_button.reset_pressing(0, True)
        else:
            self._order_button.reset_pressing(0, True)
            self._chaos_button.on_click()

        if self._mouse._right_button:
            print(self._maked_moves)

        self._undo_button.reset_pressing(self._delta_time)
        self._restart_button.reset_pressing(self._delta_time)
        self._menu_button.reset_pressing(self._delta_time)

        if self._mouse.left_button_pressing:
            if self._menu_button.check_if_clicked(self._mouse.position):
                self._game_state = "menu"
                # self._menu_button.on_click()
                return
            if self._restart_button.check_if_clicked(self._mouse.position):
                self._restart_button.on_click()
                self._start_game()
                return
            if self._undo_button.check_if_clicked(self._mouse.position):
                self._undo_button.on_click()
                if self._current_role != self._bot_role and not self._winner:
                    last_two_moves = list()
                    if len(self._maked_moves) > 0:
                        last_two_moves.append(self._maked_moves.pop()[0])
                        last_two_moves.append(self._maked_moves.pop()[0])
                        self._board.undo_moves(last_two_moves)
                        self._bot.undo_moves()

        if self._winner:  # game has ended
            return

        if self._current_role == self._bot_role:
            self._bot_clock -= self._delta_time
            if self._bot_clock <= 0:
                bot_move = self._bot.make_move(self._bot_role)
                print(f'\t<=: {bot_move}')
                if self._board.update(bot_move[0], bot_move[1]):
                    self._maked_moves.append(bot_move)
                    self._winner = self._bot.check_winning()
                    if self._winner:
                        print(f'{self._winner} won! gg!')
                    self._current_role = _return_oposite_role(self._current_role)
                    self._bot_clock = self._bot_time_delay
                    # self._bot_role = _return_oposite_role(self._bot_role)  # bot vs bot
                    return

        if self._mouse.left_button_pressing:
            if self._circle_button.check_if_clicked(self._mouse.position):
                self._selected_symbol = self._circle_button.on_click()
                self._cross_button.update_colors(("", "black"))

            if self._cross_button.check_if_clicked(self._mouse.position):
                self._selected_symbol = self._cross_button.on_click()
                self._circle_button.update_colors(("", "black"))

            if self._current_role != self._bot_role:
                cell_index = self._board.calculate_cell_index(self._mouse.position)
                if not cell_index[0]:  # calculated index is not correct (mouse was outside the game board etc.)
                    return
                if self._board.update(cell_index[1], self._selected_symbol):
                    self._maked_moves.append((cell_index[1], f'p_{self._selected_symbol}'))
                    self._winner = self._bot.check_winning()
                    if self._winner:
                        print(f'{self._winner} won! gg!')
                    self._current_role = _return_oposite_role(self._current_role)
                    return

    def _game_render(self) -> None:
        self._screen.fill(pygame.Color(0, 255, 153))

        self._board.render_board(self._screen)
        self._cross_button.render(self._screen)
        self._circle_button.render(self._screen)
        self._order_button.render(self._screen)
        self._chaos_button.render(self._screen)
        self._undo_button.render(self._screen)
        self._restart_button.render(self._screen)
        self._menu_button.render(self._screen)
        if self._winner:
            pass  # render overlay over board "chaos/order won"
        pygame.display.flip()
