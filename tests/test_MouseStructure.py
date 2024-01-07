from MouseStructure import Mouse


def test_reset_mouse_pressing():
    mouse = Mouse()
    mouse._right_button = True
    mouse._left_button = True
    mouse.reset_mouse_pressing()
    assert mouse.right_button_pressing is False
    assert mouse.left_button_pressing is False
