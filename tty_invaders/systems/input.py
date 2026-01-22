"""Input handling system."""
from typing import Any


class InputState:
    """Tracks current input state."""

    def __init__(self) -> None:
        """Initialize input state."""
        self.move_left = False
        self.move_right = False
        self.shoot = False
        self.pause = False
        self.quit = False

    def reset(self) -> None:
        """Reset all input flags."""
        self.move_left = False
        self.move_right = False
        self.shoot = False
        self.pause = False
        self.quit = False


def process_gameplay_input(key: Any, input_state: InputState) -> None:
    """Process input during gameplay.

    Args:
        key: Key object from blessed
        input_state: InputState to update
    """
    input_state.reset()

    if not key:
        return

    # Movement
    if key.name == "KEY_LEFT" or key == "a":
        input_state.move_left = True
    elif key.name == "KEY_RIGHT" or key == "d":
        input_state.move_right = True

    # Shooting
    if key == " " or key.name == "KEY_ENTER":
        input_state.shoot = True

    # Pause
    if key == "p" or key.name == "KEY_ESCAPE":
        input_state.pause = True

    # Quit
    if key == "q":
        input_state.quit = True
