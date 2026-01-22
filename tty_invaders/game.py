"""Main game class and loop orchestration."""
from typing import Any

from .config import FPS
from .renderer.terminal import Terminal
from .utils.timer import GameTimer
from .states.base import StateManager
from .states.menu import MenuState
from .audio.sound import SoundManager


class Game:
    """Main game orchestrator."""

    def __init__(self) -> None:
        """Initialize the game."""
        self.terminal = Terminal()
        self.timer = GameTimer(FPS)
        self.state_manager = StateManager(self)
        self.sound_manager = SoundManager()
        self.running = False
        self.score = 0
        self.high_score = 0
        self.lives = 0
        self.level = 1

    def initialize(self) -> bool:
        """Initialize game systems.

        Returns:
            True if initialization successful, False otherwise
        """
        # Check terminal size
        is_valid, error = self.terminal.check_size()
        if not is_valid:
            print(error)
            return False

        # Initialize states
        self._setup_states()

        return True

    def _setup_states(self) -> None:
        """Setup all game states."""
        # Import states here to avoid circular imports
        from .states.menu import MenuState
        from .states.playing import PlayingState
        from .states.paused import PausedState
        from .states.game_over import GameOverState
        from .states.leaderboard import LeaderboardState
        from .states.options import OptionsState
        from .utils.persistence import HighScoreManager
        from .utils.settings import GameSettings

        # Load high scores
        hsm = HighScoreManager()
        self.high_score = hsm.get_top_score()

        # Load settings
        self.settings = GameSettings()

        # Update sound manager with settings
        sound_enabled = self.settings.get("sound_enabled", True)
        self.sound_manager.enabled = sound_enabled

        # Add states
        self.state_manager.add_state("menu", MenuState(self))
        self.state_manager.add_state("playing", PlayingState(self))
        self.state_manager.add_state("paused", PausedState(self))
        self.state_manager.add_state("game_over", GameOverState(self))
        self.state_manager.add_state("leaderboard", LeaderboardState(self))
        self.state_manager.add_state("options", OptionsState(self))

        # Start with menu
        self.state_manager.change_state("menu")

    def run(self) -> None:
        """Run the main game loop."""
        self.running = True
        last_width = self.terminal.width
        last_height = self.terminal.height

        try:
            with self.terminal.fullscreen(), \
                 self.terminal.cbreak(), \
                 self.terminal.hidden_cursor():

                while self.running:
                    # Calculate delta time
                    dt = self.timer.tick()

                    # Check for terminal resize
                    if self.terminal.width != last_width or self.terminal.height != last_height:
                        last_width = self.terminal.width
                        last_height = self.terminal.height
                        # Terminal was resized, clear screen for clean redraw
                        self.terminal.clear()

                    # Handle input (non-blocking)
                    key = self.terminal.inkey(timeout=0)
                    self.state_manager.handle_input(key)

                    # Update game state
                    self.state_manager.update(dt)

                    # Render
                    self.terminal.clear()
                    self.state_manager.render(self.terminal)
                    self.terminal.flush()

                    # Wait for next frame
                    self.timer.wait_for_next_frame()

        except KeyboardInterrupt:
            # Clean exit on Ctrl+C
            pass

    def reset_game(self) -> None:
        """Reset game to initial state for new game."""
        from .config import PLAYER_LIVES

        self.score = 0
        self.lives = PLAYER_LIVES
        self.level = 1
