import pygame


class Button:
    def __init__(self, size=(32, 32), position=(0, 0), fill_color="black", border_color="white") -> None:
        self._size = size
        self._position = position
        self._fill_color = fill_color
        self._border_color = border_color

    def update_position(self, position: (int, int)) -> None:
        self._position = position

    def update_size(self, size: (int, int)) -> None:
        self._size = size

    def update_colors(self, colors: (str, str)) -> None:
        if colors[0]:
            self._fill_color = colors[0]
        if colors[1]:
            self._border_color = colors[1]

    def check_if_clicked(self, mouse_position: (int, int)) -> bool:
        if mouse_position[0] >= self._position[0] and mouse_position[0] <= self._position[0]+self._size[0]:
            if mouse_position[1] >= self._position[1] and mouse_position[1] <= self._position[1]+self._size[1]:
                return True
        return False

    def on_click(self) -> None:
        self.update_colors(("", "yellow"))

    def render(self, screen: pygame.surface) -> None:
        button_rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, self._fill_color, button_rect, 0, 10)
        pygame.draw.rect(screen, self._border_color,  button_rect, 3, 10)


class ChangeSymbolButton(Button):
    def __init__(self, symbol) -> None:
        super().__init__()
        self._symbol = symbol

    def on_click(self) -> None:
        self.update_colors(("", "yellow"))
        return self._symbol
