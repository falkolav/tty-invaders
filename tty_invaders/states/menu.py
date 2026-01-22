"""Main menu state."""
from typing import Any

from .base import BaseState
from ..renderer.terminal import Terminal
from ..renderer.ui import render_menu


class MenuState(BaseState):
    """Main menu state."""

    def __init__(self, game: Any) -> None:
        """Initialize menu state.

        Args:
            game: Reference to the main game instance
        """
        super().__init__(game)
        self.selected_option = 0
        self.options = ["Start Game", "Options", "Leaderboard", "Quit"]

    def enter(self) -> None:
        """Called when entering menu state."""
        self.selected_option = 0

    def exit(self) -> None:
        """Called when exiting menu state."""
        pass

    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        if not key:
            return

        if key.name == "KEY_UP" or key == "w":
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key.name == "KEY_DOWN" or key == "s":
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key.name == "KEY_ENTER" or key == " ":
            self._select_option()
        elif key == "q" or key.name == "KEY_ESCAPE":
            self.game.running = False

    def _select_option(self) -> None:
        """Handle option selection."""
        option = self.options[self.selected_option]

        if option == "Start Game":
            self.game.state_manager.change_state("playing")
        elif option == "Options":
            self.game.state_manager.change_state("options")
        elif option == "Leaderboard":
            self.game.state_manager.change_state("leaderboard")
        elif option == "Quit":
            self.game.running = False

    def update(self, dt: float) -> None:
        """Update menu logic.

        Args:
            dt: Delta time in seconds
        """
        # Menu is static, no update needed
        pass

    def render(self, term: Terminal) -> None:
        """Render the menu.

        Args:
            term: Terminal instance
        """
        title = "TTY INVADERS"
        options = [(opt, i == self.selected_option) for i, opt in enumerate(self.options)]
        footer = "Use ↑↓ or WS to navigate, ENTER/SPACE to select, Q/ESC to quit"

        render_menu(term, title, options, footer)
