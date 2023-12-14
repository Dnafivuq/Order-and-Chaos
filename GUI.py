import pygame


class Button:
    def __init__(self) -> None:
        self._size = (32, 32)
        self._fill_color = "black"
        self._border_color = "white"
        self._position = (0, 0)

    def update_position(self, position):
        self._position = position

    def update_size(self, size):
        self._size = size

    def update_colors(self, colors):
        self._fill_color = colors[0]
        self._border_color = colors[1]

    def check_if_clicked(self, mouse_position) -> bool:
        if mouse_position[0] >= self._position[0] and mouse_position[0] <= self._position[0]+self._size[0]:
            if mouse_position[1] >= self._position[1] and mouse_position[1] <= self._position[1]+self._size[0]:
                return True
        return False

    def on_click(self) -> None:
        pass

    def render(self, screen):
        button_rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, self._fill_color, button_rect, 0, 10)
        pygame.draw.rect(screen, self._border_color,  button_rect, 3, 10)


class ChangeSymbolButton(Button):
    def __init__(self, symbol) -> None:
        super().__init__()
        self._symbol = symbol

    def on_click(self):
        self.update_colors((self._fill_color, "yellow"))
        return self._symbol
