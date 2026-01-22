"""Leaderboard state."""
from typing import Any

from .base import BaseState
from ..renderer.terminal import Terminal
from ..config import GAME_WIDTH, COLOR_UI


class LeaderboardState(BaseState):
    """Leaderboard display state."""

    def __init__(self, game: Any) -> None:
        """Initialize leaderboard state.

        Args:
            game: Reference to the main game instance
        """
        super().__init__(game)

    def enter(self) -> None:
        """Called when entering leaderboard state."""
        pass

    def exit(self) -> None:
        """Called when exiting leaderboard state."""
        pass

    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        if key:
            # Any key returns to menu
            self.game.state_manager.change_state("menu")

    def update(self, dt: float) -> None:
        """Update leaderboard logic.

        Args:
            dt: Delta time in seconds
        """
        pass

    def render(self, term: Terminal) -> None:
        """Render the leaderboard.

        Args:
            term: Terminal instance
        """
        from ..utils.persistence import HighScoreManager

        height = term.height
        width = GAME_WIDTH

        # Clear and draw border
        term.write_at(0, 0, "╔" + "═" * (width - 2) + "╗", COLOR_UI)
        for y in range(1, height - 1):
            term.write_at(0, y, "║", COLOR_UI)
            term.write_at(width - 1, y, "║", COLOR_UI)
        term.write_at(0, height - 1, "╚" + "═" * (width - 2) + "╝", COLOR_UI)

        # Title
        title = "HIGH SCORES"
        title_y = 2
        title_x = (width - len(title)) // 2
        term.write_at(title_x, title_y, title, "bright_cyan")

        # Load and display scores
        hsm = HighScoreManager()
        entries = hsm.get_entries()

        if not entries:
            no_scores = "No high scores yet!"
            y = height // 2
            term.write_at((width - len(no_scores)) // 2, y, no_scores, "bright_black")
        else:
            # Table header
            header = "  RANK  NAME   SCORE    LVL  MODE"
            header_y = 5
            term.write_at((width - len(header)) // 2, header_y, header, "white")

            # Separator
            separator = "  " + "─" * (len(header) - 2)
            term.write_at((width - len(separator)) // 2, header_y + 1, separator, "bright_black")

            # Entries
            start_y = header_y + 2
            for i, entry in enumerate(entries[:10], 1):
                rank = f"{i:2d}."
                name = entry.name.ljust(5)
                score = f"{entry.score:6d}"
                level = f"{entry.level:3d}"
                # Shorten game mode names for display
                mode_map = {
                    "normal": "NRM",
                    "slow_mo": "SLO",
                    "turbo": "TRB",
                    "insane": "INS",
                    "zen": "ZEN",
                    "nightmare": "NGT",
                    "superdupercrazy": "SDC"
                }
                mode_short = mode_map.get(entry.game_mode, "NRM")
                line = f"  {rank}  {name}  {score}   {level}  {mode_short}"

                color = "yellow" if i == 1 else "white" if i <= 3 else "bright_black"
                y = start_y + i - 1
                term.write_at((width - len(line)) // 2, y, line, color)

        # Footer
        footer = "Press any key to return to menu"
        footer_y = height - 3
        footer_x = (width - len(footer)) // 2
        term.write_at(footer_x, footer_y, footer, "bright_black")
