import pygame


class Button:
    def __init__(self, size=(32, 32), position=(0, 0), fill_color="black", border_color="white") -> None:
        self._size = size
        self._position = position
        self._base_fill_color = fill_color
        self._base_border_color = border_color
        self._fill_color = fill_color
        self._border_color = border_color
        self._image = ""
        self._pressing_reset_time = 0.5  # 1.5s
        self._pressing_clock = self._pressing_reset_time

    def load_image(self, path: str) -> None:
        self._image = pygame.image.load(path)

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
        self._pressing_clock = self._pressing_reset_time

    def reset_pressing(self, delta_time: float, instant_reset=False) -> None:
        self._pressing_clock -= delta_time
        if self._pressing_clock >= 0 and not instant_reset:
            return
        self.update_colors((self._base_fill_color, self._base_border_color))
        self._pressing_clock = self._pressing_reset_time

    def render(self, screen: pygame.surface) -> None:
        button_rect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, self._fill_color, button_rect, 0, 10)
        pygame.draw.rect(screen, self._border_color,  button_rect, 3, 10)
        if self._image:
            screen.blit(self._image, self._position)


class ChangeSymbolButton(Button):
    def __init__(self, symbol) -> None:
        super().__init__()
        self._symbol = symbol

    def on_click(self) -> None:
        self.update_colors(("", "yellow"))
        return self._symbol


class Text:
    def __init__(self) -> None:
        pass

    def set_text(self, text: str) -> None:
        self._text = text

    def set_font(self, font: str) -> None:
        pass
