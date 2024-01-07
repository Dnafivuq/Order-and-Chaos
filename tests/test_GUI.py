from GUI import Button


def test_button_check_if_clicked_contains():
    button = Button()
    position = (10, 10)
    assert button.check_if_clicked(position) is True


def test_button_check_if_clicked_does_not_contain():
    button = Button()
    position = (100, 10)
    assert button.check_if_clicked(position) is False
