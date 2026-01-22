"""Entry point for TTY Invaders."""
import sys

# Handle both direct execution and module execution
try:
    from .game import Game
except ImportError:
    from tty_invaders.game import Game


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    game = Game()

    if not game.initialize():
        return 1

    game.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
