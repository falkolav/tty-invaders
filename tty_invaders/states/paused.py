"""Paused state."""
from typing import Any

from .base import BaseState
from ..renderer.terminal import Terminal
from ..renderer.ui import render_paused


class PausedState(BaseState):
    """Paused game state."""

    def __init__(self, game: Any) -> None:
        """Initialize paused state.

        Args:
            game: Reference to the main game instance
        """
        super().__init__(game)
        self.previous_state_snapshot: Any = None

    def enter(self) -> None:
        """Called when entering paused state."""
        # Store reference to playing state for rendering
        if "playing" in self.game.state_manager.states:
            self.previous_state_snapshot = self.game.state_manager.states["playing"]

    def exit(self) -> None:
        """Called when exiting paused state."""
        pass

    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        if not key:
            return

        if key == "p" or key.name == "KEY_ESCAPE":
            # Resume game
            self.game.state_manager.change_state("playing")
        elif key == "q":
            # Quit to menu
            self.game.state_manager.change_state("menu")

    def update(self, dt: float) -> None:
        """Update paused logic.

        Args:
            dt: Delta time in seconds
        """
        # Paused - no updates
        pass

    def render(self, term: Terminal) -> None:
        """Render the paused screen.

        Args:
            term: Terminal instance
        """
        # Render the game state behind the pause overlay
        if self.previous_state_snapshot:
            self.previous_state_snapshot.render(term)

        # Render pause overlay
        render_paused(term)
