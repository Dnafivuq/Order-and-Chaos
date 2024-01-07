import pygame
import json
from GameBoard import GameBoard
from MouseStructure import Mouse
import GUI
from Bot import Bot


class GameEngine:
    """
    A class representing GameEnginge.
    GameEnginge contains every other module.
    It is responsible for rendering and updating other objects like GameBoard or Bot.

    ...

    Attributes
    ----------
    assets: dict
        A dictionary that hold assets paths loaded from config.json file
    delta_time: float
        A time between two frames
    screen: pygame.Surface
        Main game window
    transparent_surface: pygame.Surface
        Surface used for rendering semi-trasparent content to main window
    running: bool
        Variable responsible for keeping the game window alive (True if window is open)
    clock: pygame.Clock
        Game clock used for calculating delta time and locking framerate
    board: GameBoard
        Main game board object
    mouse: Mouse
        Main game mouse object
    maked_moves: list[tuple[int, str]]
        List containing already maked moves
    bot: Bot
        Main game bot object
    game_state: str
        Variable holding current game state
            > "menu"
            > "game"
    BUTTONS: GUI.ChangeSymbolButton
        > cross_button
            GAME: Change symbol to `cross` and indicator
        > circle_button
            GAME: Change symbol to `circle` and indicator
    BUTTONS: GUI.Button
        > order_button
            GAME: `Order` turn indicator
        > chaos_button
            GAME: `Chaos` turn indicator
        > undo_button
            GAME: Undo two last moves
        > restart_button
            GAME: Restart game
        > menu_button
            GAME: Change game state to `menu`
        > order_menu_button
            MENU: Change role to `order`
        > chaos_menu_button
            MENU: Change role to `chaos`
        > easy_menu_button
            MENU: Change difficulty to `easy`
        > hard_menu_button
            MENU: Change difficulty to `hard`
        > start_button
            MENU: Start game, change game state to `game`
    TEXTS: GUI.Text
        > your_role_text
            GAME: `(YOU)` text displayed below `order` or `chaos` buttons indicating player's role
        > winner_text
            GAME: `{winner} won! GG!` text displayed after the game end
        > game_logo_text
            MENU: Game logo text displayed in menu

    Methods
    -------
    load_assets()
        Loads assets paths to dictionary from config.json.
    start_game()
        Sets needed variables for `game` to start.
    run()
        Main game loop.
    process_events()
        Process user input.
    menu_update()
        Updates menu objects. Called when `game_state` == `menu`.
    menu_render()
        Renders menu objects. Called when `game_state` == `menu`.
    game_update()
        Updates game objects. Called when `game_state` == `game`.
    game_render()
        Renders game objects. Called when `game_state` == `game`.
    """

    def __init__(self) -> None:
        self._assets = dict()
        self._load_assets()
        self._delta_time = 0
        self._screen = pygame.display.set_mode((960, 720))
        self._transparent_surface = pygame.Surface((960, 720), pygame.SRCALPHA)
        pygame.display.set_caption("ORDER AND CHAOS")
        self._running = True
        self._clock = pygame.time.Clock()
        self._board = GameBoard()
        self._board.load_symbols_texture(self._assets['cross_img'], self._assets['circle_img'])
        self._mouse = Mouse()

        self._maked_moves = list()

        self._bot = Bot()
        self._bot_difficulty = "hard"
        self._bot_role = "order"

        self._game_state = "menu"

        self._cross_button = GUI.ChangeSymbolButton("cross")
        self._cross_button.update_position((740, 316))
        self._cross_button.update_size((64, 64))
        self._cross_button.update_colors(("grey", "black"))
        self._cross_button.load_image(self._assets['cross_img'])

        self._circle_button = GUI.ChangeSymbolButton("circle")
        self._circle_button.update_position((740+96, 316))
        self._circle_button.update_size((64, 64))
        self._circle_button.update_colors(("grey", "black"))
        self._circle_button.load_image(self._assets['circle_img'])

        self._order_menu_button = GUI.Button((96, 96), (291, 145+47), "light blue", "black")
        self._chaos_menu_button = GUI.Button((96, 96), (574, 145+47), "light blue", "black")
        self._chaos_menu_button.on_click()  # by deafult picked role is chaos

        self._easy_menu_button = GUI.Button((96, 96), (291, 145+190+35+47), "light blue", "black")
        self._hard_menu_button = GUI.Button((96, 96), (574, 145+190+35+47), "light blue", "black")
        self._hard_menu_button.on_click()  # by deafult difficulty is hard

        self._order_button = GUI.Button((64, 64), (740, 120), "light blue", "black")
        self._order_button.load_image(self._assets['order_img'])
        self._order_button.change_image_scaling(2/3)

        self._chaos_button = GUI.Button((64, 64), (740+96, 120), "light blue", "black")
        self._chaos_button.load_image(self._assets['chaos_img'])
        self._chaos_button.change_image_scaling(2/3)

        self._undo_button = GUI.Button((164, 50), (740, 430), "light blue", "black")
        self._undo_button.load_image(self._assets['undo_img'])

        self._restart_button = GUI.Button((164, 50), (740, 430+80), "light blue", "black")
        self._restart_button.load_image(self._assets['restart_img'])

        self._menu_button = GUI.Button((164, 50), (740, 430+160), "light blue", "black")
        self._menu_button.load_image(self._assets['menu_img'])

        self._start_button = GUI.Button((164, 50), (398, 600), "light blue", "black")
        self._start_button.load_image(self._assets['start_img'])

        self._game_logo_text = GUI.Text()
        self._game_logo_text.set_font(self._assets['font_path'], 64)
        self._game_logo_text.set_text("Order And Chaos")
        self._game_logo_text.set_text_position((198, 35))

        self._your_role_text = GUI.Text()
        self._your_role_text.set_font(self._assets['font_path'], 20)
        self._your_role_text.set_text("(YOU)")

        self._winner_text = GUI.Text(66)

    def _load_assets(self) -> None:
        """
        Loads assets paths to dictionary `assets` from config.json.

        Raises
        ------
        FileNotFoundError
            If `config.json` file is missing
        """

        with open("config.json") as json_file:
            self._assets = json.load(json_file)

    def _start_game(self):
        """
        Sets needed variables for `game` to start.
        Called on game start and restart.
        """

        self._current_role = "order"
        self._selected_symbol = self._circle_button.on_click()
        self._cross_button.update_colors(("", "black"))
        self._winner = ""

        self._game_state = "game"

        self._maked_moves.clear()
        self._mouse.reset_mouse_pressing()

        self._board.set_up_board()

        if self._bot_role == "order":
            self._your_role_text.set_text_position((741+96, 120+70))
        else:
            self._your_role_text.set_text_position((741, 120+70))

        self._bot.load_board(self._board.board)
        self._bot.set_difficulty(self._bot_difficulty)
        self._bot_time_delay = 1.5  # 1.5s
        self._bot_clock = self._bot_time_delay

    def run(self) -> None:
        """
        Main game loop.
        Method that needs to be called for application to start.
        """

        self._delta_time = self._clock.tick(60) / 1000
        while (self._running):
            self._process_events()
            if self._game_state == "menu":
                self._menu_update()
                self._menu_render()
            elif self._game_state == "game":
                self._game_update()
                self._game_render()

    def _process_events(self) -> None:
        """
        Process user input.
        """

        self._mouse.reset_mouse_pressing()
        for event in pygame.event.get():
            self._mouse.update_mouse_position(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
                self._mouse._left_button = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 3:
                self._mouse._right_button = True

    def _menu_update(self) -> None:
        """
        Updates menu objects. Called when `game_state` == `menu`.
        """

        if self._mouse.left_button_pressing:
            if self._order_menu_button.check_if_clicked(self._mouse.position):
                self._bot_role = "chaos"
                self._order_menu_button.on_click()
                self._chaos_menu_button.reset_pressing(0, True)

            if self._chaos_menu_button.check_if_clicked(self._mouse.position):
                self._bot_role = "order"
                self._chaos_menu_button.on_click()
                self._order_menu_button.reset_pressing(0, True)

            if self._easy_menu_button.check_if_clicked(self._mouse.position):
                self._bot_difficulty = "easy"
                self._easy_menu_button.on_click()
                self._hard_menu_button.reset_pressing(0, True)

            if self._hard_menu_button.check_if_clicked(self._mouse.position):
                self._bot_difficulty = "hard"
                self._hard_menu_button.on_click()
                self._easy_menu_button.reset_pressing(0, True)

            if self._start_button.check_if_clicked(self._mouse.position):
                self._start_game()
        return

    def _menu_render(self) -> None:
        """
        Renders menu objects. Called when `game_state` == `menu`.
        """

        self._screen.fill(pygame.Color(0, 255, 153))
        pygame.draw.polygon(self._screen, (255, 255, 82), ((0, 0), (960, 720), (0, 720)))

        buttons_space_rect = pygame.Rect(116, 145, 729, 190)
        pygame.draw.rect(self._screen, pygame.Color(0, 181, 108), buttons_space_rect, 0, 10)
        buttons_space_rect.y = 145+190+35
        pygame.draw.rect(self._screen, pygame.Color(0, 181, 108), buttons_space_rect, 0, 10)

        text_space_rect = pygame.Rect(116+35, 145+63, 140, 64)
        pygame.draw.rect(self._screen, pygame.Color(0, 217, 130), text_space_rect)
        text_space_rect.x = 670
        pygame.draw.rect(self._screen, pygame.Color(0, 217, 130), text_space_rect)
        text_space_rect.y = 370+63
        pygame.draw.rect(self._screen, pygame.Color(0, 217, 130), text_space_rect)
        text_space_rect.x = 116+35
        pygame.draw.rect(self._screen, pygame.Color(0, 217, 130), text_space_rect)

        menu_buttons_text = GUI.Text(30)
        menu_buttons_text.set_text("ORDER")
        menu_buttons_text.set_text_center_position((220, 240))
        menu_buttons_text.render(self._screen)

        menu_buttons_text.set_text("CHAOS")
        menu_buttons_text.set_text_center_position((740, 240))
        menu_buttons_text.render(self._screen)

        menu_buttons_text.set_text("EASY")
        menu_buttons_text.set_text_center_position((220, 464))
        menu_buttons_text.render(self._screen)

        menu_buttons_text.set_text("HARD")
        menu_buttons_text.set_text_center_position((740, 464))
        menu_buttons_text.render(self._screen)

        menu_buttons_placeholder_text = GUI.Text(40)

        menu_buttons_placeholder_text.set_text("YOUR ROLE")
        menu_buttons_placeholder_text.set_text_center_position((480, 240))
        menu_buttons_placeholder_text.render(self._screen)

        menu_buttons_placeholder_text.set_text("DIFFICULTY")
        menu_buttons_placeholder_text.set_text_center_position((480, 464))
        menu_buttons_placeholder_text.render(self._screen)
        # pygame.draw.rect(screen, pygame.Color(26, 26, 26), cell_Rect, 3, 10)
        self._order_menu_button.render(self._screen)
        self._chaos_menu_button.render(self._screen)
        self._easy_menu_button.render(self._screen)
        self._hard_menu_button.render(self._screen)
        self._start_button.render(self._screen)
        self._game_logo_text.render(self._screen)
        pygame.display.flip()

    def _game_update(self) -> None:
        """
        Updates game objects. Called when `game_state` == `game`.
        """

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

        # printing of already maked moves
        # if self._mouse._right_button:
        #     print(self._maked_moves)

        self._undo_button.reset_pressing(self._delta_time)
        self._restart_button.reset_pressing(self._delta_time)
        self._menu_button.reset_pressing(self._delta_time)

        if self._mouse.left_button_pressing:
            if self._menu_button.check_if_clicked(self._mouse.position):
                self._game_state = "menu"
                return
            if self._restart_button.check_if_clicked(self._mouse.position):
                self._restart_button.on_click()
                self._start_game()
                return
            if self._undo_button.check_if_clicked(self._mouse.position):
                self._undo_button.on_click()
                if self._current_role != self._bot_role and (len(self._maked_moves) > 1) and not self._winner:
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
                if self._board.update(bot_move[0], bot_move[1]):
                    self._maked_moves.append(bot_move)
                    self._winner = self._bot.check_winning()
                    if self._winner:
                        self._winner_text.set_text(f'{self._winner} won! GG!')
                        self._winner_text.set_text_center_position((360, 360))
                    self._current_role = _return_oposite_role(self._current_role)
                    self._bot_clock = self._bot_time_delay
                    # self._bot_role = _return_oposite_role(self._bot_role)  # bot vs bot
                    # this feature is not fully supported therefore it is not included in menu or anywhere else
                    # In order to turn on, uncomment the line. Recommended to change difficulty to hard.
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
                if not cell_index[0]:  # calculated index is not correct (mouse was outside the game board)
                    return
                if self._board.update(cell_index[1], self._selected_symbol):
                    self._maked_moves.append((cell_index[1], f'p_{self._selected_symbol}'))
                    self._winner = self._bot.check_winning()
                    if self._winner:
                        self._winner_text.set_text(f'{self._winner} won! GG!')
                        self._winner_text.set_text_center_position((360, 360))
                    self._current_role = _return_oposite_role(self._current_role)
                    return

    def _game_render(self) -> None:
        """
        Renders game objects. Called when `game_state` == `game`.
        """

        self._screen.fill(pygame.Color(0, 255, 153))

        self._board.render(self._screen)
        self._cross_button.render(self._screen)
        self._circle_button.render(self._screen)
        self._order_button.render(self._screen)
        self._chaos_button.render(self._screen)
        self._undo_button.render(self._screen)
        self._restart_button.render(self._screen)
        self._menu_button.render(self._screen)
        self._your_role_text.render(self._screen)
        if self._winner:
            winner_space_rect = pygame.Rect(42, 42, 636, 636)
            pygame.draw.rect(self._transparent_surface, pygame.Color(200, 217, 130, 180), winner_space_rect)
            self._screen.blit(self._transparent_surface, (0, 0))
            self._winner_text.render(self._screen)
        pygame.display.flip()
