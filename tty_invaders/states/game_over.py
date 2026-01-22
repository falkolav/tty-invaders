"""Game over state."""
from typing import Any

from .base import BaseState
from ..renderer.terminal import Terminal
from ..renderer.ui import render_game_over
from ..config import GAME_WIDTH


class GameOverState(BaseState):
    """Game over state with optional name entry."""

    def __init__(self, game: Any) -> None:
        """Initialize game over state.

        Args:
            game: Reference to the main game instance
        """
        super().__init__(game)
        self.sound_manager = game.sound_manager
        self.is_high_score = False
        self.entering_name = False
        self.player_name = ""
        self.wait_time = 0.0

    def enter(self) -> None:
        """Called when entering game over state."""
        # Check if this is a high score
        from ..utils.persistence import HighScoreManager

        self.sound_manager.play_game_over()

        hsm = HighScoreManager()
        self.is_high_score = hsm.is_high_score(self.game.score)

        if self.is_high_score:
            self.entering_name = True
            self.player_name = ""
        else:
            self.entering_name = False

        self.wait_time = 0.0

    def exit(self) -> None:
        """Called when exiting game over state."""
        pass

    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        if not key:
            return

        if self.entering_name:
            # Name entry mode
            if key.name == "KEY_ENTER" or key == " ":
                if len(self.player_name) == 3:
                    self._save_high_score()
                    self.entering_name = False
            elif key.name == "KEY_BACKSPACE" or key.name == "KEY_DELETE":
                if self.player_name:
                    self.player_name = self.player_name[:-1]
            elif key.isalpha() and len(self.player_name) < 3:
                self.player_name += key.upper()
        else:
            # Return to menu after showing score
            if self.wait_time > 2.0:  # Wait at least 2 seconds
                self.game.state_manager.change_state("menu")

    def _save_high_score(self) -> None:
        """Save the high score."""
        from ..utils.persistence import HighScoreManager

        hsm = HighScoreManager()
        game_mode = self.game.settings.get("game_mode", "normal")
        hsm.add_score(self.player_name, self.game.score, self.game.level, game_mode)

        # Update game high score
        self.game.high_score = hsm.get_top_score()

    def update(self, dt: float) -> None:
        """Update game over logic.

        Args:
            dt: Delta time in seconds
        """
        self.wait_time += dt

    def render(self, term: Terminal) -> None:
        """Render the game over screen.

        Args:
            term: Terminal instance
        """
        render_game_over(term, self.game.score, self.is_high_score)

        if self.entering_name:
            # Show name entry prompt
            prompt = "Enter name (3 letters):"
            name_display = self.player_name + "_" * (3 - len(self.player_name))

            y = term.height // 2 + 4
            term.write_at((GAME_WIDTH - len(prompt)) // 2, y, prompt, "white")
            term.write_at((GAME_WIDTH - len(name_display)) // 2, y + 2, name_display, "yellow")
        else:
            # Show continue prompt
            if self.wait_time > 2.0:
                prompt = "Press any key to continue"
                y = term.height // 2 + 4
                term.write_at((GAME_WIDTH - len(prompt)) // 2, y, prompt, "bright_black")
