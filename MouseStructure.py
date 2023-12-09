import pygame


class Mouse:
    def __init__(self) -> None:
        self._position = pygame.Vector2(0, 0)
        self._right_button = False
        self._left_button = False

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @property
    def right_button_pressing(self) -> bool:
        return self._right_button

    @property
    def left_button_pressing(self) -> bool:
        return self._left_button

    def update_mouse_position(self, new_position: pygame.Vector2) -> None:
        self._position = new_position

    def reset_mouse_pressing(self):
        self._right_button = False
        self._left_button = False
