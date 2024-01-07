import pygame


class Button:
    """
    A class used to represent a GUI button.

    ...

    Attributes
    ----------
    size: tuple[int, int]
        The size of the the button
    position: tuple[int, int]
        The position of the button
    base_fill_color: str
        The not-activated, deafult color of button filling
    base_border_color: str
        The not-activated, deafult color of button border
    fill_color: str
        The current color of button filling
    border_color: str
        The current color of button border
    image: pygame.image
        The button image (By deafult None)
    pressing_reset_time: float
        Time that takes button to reset it's pressing (in seconds)
    pressing_clock: float
        Button internal clock for pressing reset

    Methods
    -------
    load_image(path: str)
        Loads image.
    update_position(position: tuple[int, int])
        Updates the button position to a given position.
    update_size(size: tuple[int, int])
        Updates the button size.
    update_colors(self, colors: tuple[str, str])
        Updates button filling and border color.
    change_image_scaling(factor: float)
        Changes current image size by a scaling factor.
    check_if_clicked(mouse_position: tuple[int, int]):
        Checks if the button contains the mouse position.
    on_click()
        The button method when clicked.
    reset_pressing(delta_time: float, instant_reset=False)
        Resets the button pressing.
    render(screen: pygame.surface)
        Rendering the button to a surface.
    """

    def __init__(self, size=(32, 32), position=(0, 0),
                 fill_color="white", border_color="black",
                 pressing_reset_time=0.5) -> None:
        """
        Parameters
        ----------
        size: tuple[int, int], optional
            The size of the the button (deafult (32, 32))
        position: tuple[int, int], optional
            The position of the button (deafult (0, 0))
        fill_color: str, optional
            The current color of button filling (deafult 'white')
        border_color: str, optional
            The current color of button border (deafult 'black')
        pressing_reset_time: float, optional
            Time (in seconds) that takes button to reset it's pressing (deafult 0.5)
        """

        self._size = size
        self._position = position
        self._base_fill_color = fill_color
        self._base_border_color = border_color
        self._fill_color = fill_color
        self._border_color = border_color
        self._image = None
        self._pressing_reset_time = pressing_reset_time  # 0.5 meaning 0.5s
        self._pressing_clock = self._pressing_reset_time

    def load_image(self, path: str) -> None:
        """
        Loads image for button.
        Function does not handle wrong image paths.

        Raises
        ------
        FileNotFoundError
            If no image is found by given path.

        Parameters
        ----------
        path: str
            Path to the image
        """

        self._image = pygame.image.load(path)

    def update_position(self, position: tuple[int, int]) -> None:
        """
        Updates the button's position to given.

        Parameters
        ----------
        position: tuple[int, int]
            New button position
        """

        self._position = position

    def update_size(self, size: tuple[int, int]) -> None:
        """
        Updates the button's size to given.

        Parameters
        ----------
        size: tuple[int, int]
            New button size
        """

        self._size = size

    def update_colors(self, colors: tuple[str, str]) -> None:
        """
        Updates the button's colors to given, if a color is not passed,
        the function does not update it.

        Parameters
        ----------
        size: tuple[str, str]
            New button colors [fill_color, border_color]
        """

        if colors[0]:
            self._fill_color = colors[0]
        if colors[1]:
            self._border_color = colors[1]

    def change_image_scaling(self, factor: float) -> None:
        """
        If image is loaded, the function changes current
        image size by a scaling factor, otherwise it skips.

        Parameters
        ----------
        factor: float
            Image scaling factor
        """
        if self._image is not None:
            self._image = pygame.transform.scale_by(self._image, factor)

    def check_if_clicked(self, mouse_position: tuple[int, int]) -> bool:
        """
        Checks if the button contains the mouse position.
        The function does not now if mouse button was pressed, so in reality it only checks
        if mouse hovers over the button.

        Parameters
        ----------
        mouse_position: tuple[int, int]
            The mouse position

        Returns
        -------
        bool
            True if the button contains the mouse position, else returns False
        """

        if mouse_position[0] >= self._position[0] and mouse_position[0] <= self._position[0]+self._size[0]:
            if mouse_position[1] >= self._position[1] and mouse_position[1] <= self._position[1]+self._size[1]:
                return True
        return False

    def on_click(self) -> None:
        """
        The button method when clicked.
        Updates border color and starts pressing reset timer.
        """

        self.update_colors(("", "yellow"))
        self._pressing_clock = self._pressing_reset_time

    def reset_pressing(self, delta_time: float, instant_reset=False) -> None:
        """
        Updates the button pressing internal clock and resets when clock reaches 0.

        If the argument `instant_reset` is passed in, the resetting happens instantly,
        skipping the remaining time in clock.

        Parameters
        ----------
        delta_time: float
            Time (in seconds) that elapsed since last update
        instant_reset: bool, optional
            If True, the button pressing is restarted instantly and clock reseted
        """

        self._pressing_clock -= delta_time
        if self._pressing_clock >= 0 and not instant_reset:
            return
        self.update_colors((self._base_fill_color, self._base_border_color))
        self._pressing_clock = self._pressing_reset_time

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the button to given surface.

        Parameters
        ----------
        screen: pygame.Surface
            Surface that the button will be rendered to
        """

        button_rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, self._fill_color, button_rect, 0, 10)
        pygame.draw.rect(screen, self._border_color,  button_rect, 3, 10)
        if self._image is not None:
            screen.blit(self._image, self._position)


class ChangeSymbolButton(Button):
    """
    A class used to represent a GUI button for symbol changing.
    Inherits from `Button` class.

    ...

    Attributes
    ----------
    symbol: str
        Symbol that the button represents

    Methods
    -------
    on_click()
        The button method when clicked,
        overloaded `on_click()` `Button` method
    """

    def __init__(self, symbol) -> None:
        """
        Parameters
        ----------
        symbol: str
            Symbol that the button will represent
        """

        super().__init__()
        self._symbol = symbol

    def on_click(self) -> str:
        """
        The button method when clicked, overloaded `on_click()` `Button` method.
        Updates border color and returns the button symbol.

        Returns
        -------
        str
            Symbol that the button represents
        """

        self.update_colors(("", "yellow"))
        return self._symbol


class Text:
    """
    A class used to represent a GUI text.

    ...

    Attributes
    ----------
    font: pygame.Font
        The text's font
    text: pygame.Surface
        A surface that holds the text
    text_rect: pygame.Rect
        A rect for text rendering

    Methods
    -------
    def set_text(text: str, text_color='black')
        Sets the text's content to a given text.
    set_font(font: str, size: int)
        Sets the text's font to given font and size.
    set_deafult_font(size: int)
        Resets font to deafult font and given size.
    set_text_position(position: tuple[int, int])
        Updates the text's position to given position.
    set_text_center_position(position: tuple[int, int])
        Updates the text's center position to given position.
    render(screen: pygame.Surface)
        Rendering the text to a surface.
    """

    def __init__(self, size=30) -> None:
        """
        Parameters
        ----------
        size: int, optional
            The size of the text (deafult 30)
        """

        self._font = pygame.font.SysFont('timesnewroman',  size)
        self._text = self._font.render("blank_text", True, 'black')
        self._text_rect = self._text.get_rect()

    def set_text(self, text: str, text_color='black') -> None:
        """
        Sets the text's content to a given text.

        Parameters
        ----------
        text: str
            The text that will be displayed
        text_color: str, optional
            The displayed text color (deafult 'black')
        """

        self._text = self._font.render(text, True, text_color)
        self._text_rect = self._text.get_rect()

    def set_font(self, font: str, size=30) -> None:
        """
        Sets the text's font to given font and size.
        The `set_text()` method must be called after changing font to update text.

        Parameters
        ----------
        font: str
            The font that will be used for text displaying
        size: int, optional
            The size of the text (deafult 30)
        """

        self._font = pygame.font.Font(font, size)

    def set_deafult_font(self, size=30) -> None:
        """
        Resets font to deafult font and given size.
        The `set_text()` method must be called after changing font to update text.

        Parameters
        ----------
        size: int, optional
            The size of the text (deafult 30)
        """

        self._font = pygame.font.SysFont('timesnewroman',  size)

    def set_text_position(self, position: tuple[int, int]) -> None:
        """
        Updates the text's position to given position.
        Position is set by origin point (0, 0).

        Parameters
        ----------
        position: tuple[int, int]
            New text position
        """

        self._text_rect.x = position[0]
        self._text_rect.y = position[1]

    def set_text_center_position(self, position: tuple[int, int]) -> None:
        """
        Updates the text's position to given position.
        Position is set by origin point [text centre (half_size, half_size)].

        Parameters
        ----------
        position: tuple[int, int]
            New text position
        """

        self._text_rect.center = position

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the text to given surface.

        Parameters
        ----------
        screen: pygame.Surface
            Surface that the text will be rendered to
        """
        screen.blit(self._text, self._text_rect)
