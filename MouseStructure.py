class Mouse:
    """
    A class representing the mouse.

    ...

    Attributes
    ----------
    position : tuple[int, int]
        The mouse position
    right_button : bool
        The right mouse button pressing (True if pressed)
    left_button : bool
        The left mouse button pressing (True if pressed)

    Methods
    -------
    position()
        Returns mouse's position.
    right_button_pressing()
        Returns right mouse's button pressing.
    left_button_pressing()
        Returns left mouse's button pressing.
    update_mouse_position(new_position: tuple[int, int])
        Updates mouse's position.
    reset_mouse_pressing()
        Resets mouse's buttons pressing.
    """

    def __init__(self) -> None:
        self._position = (0, 0)
        self._right_button = False
        self._left_button = False

    @property
    def position(self) -> tuple[int, int]:
        """
        Returns
        -------
        tuple[int, int]
            Mouse position
        """

        return self._position

    @property
    def right_button_pressing(self) -> bool:
        """
        Returns
        -------
        bool
            Right mouse button pressing (True if pressed)
        """

        return self._right_button

    @property
    def left_button_pressing(self) -> bool:
        """
        Returns
        -------
        bool
            Left mouse left button pressing (True if pressed)
        """

        return self._left_button

    def update_mouse_position(self, new_position: tuple[int, int]) -> None:
        """
        Updates mouse position to given position.

        Parameters
        ----------
        new_position: tuple[int, int]
            New mouse position
        """

        self._position = new_position

    def reset_mouse_pressing(self):
        """
        Resets both of mouse's buttons pressing. (Sets to False)
        """

        self._right_button = False
        self._left_button = False
