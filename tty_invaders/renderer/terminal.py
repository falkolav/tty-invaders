"""Terminal wrapper using blessed for cross-platform terminal control."""
from typing import Any, Optional
from blessed import Terminal as BlessedTerminal

from ..config import MIN_TERMINAL_WIDTH, MIN_TERMINAL_HEIGHT


class Terminal:
    """Wrapper around blessed Terminal with game-specific functionality."""

    def __init__(self) -> None:
        """Initialize the terminal."""
        self.term = BlessedTerminal()
        self._buffer: list[str] = []

    @property
    def x_offset(self) -> int:
        """Calculate horizontal offset to center game.

        Returns:
            Horizontal offset in characters to center the game area
        """
        from ..config import GAME_WIDTH
        if self.term.width > GAME_WIDTH:
            return (self.term.width - GAME_WIDTH) // 2
        return 0

    def check_size(self) -> tuple[bool, str]:
        """Check if terminal meets minimum size requirements.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.term.width < MIN_TERMINAL_WIDTH or self.term.height < MIN_TERMINAL_HEIGHT:
            return False, (
                f"Terminal too small! Need {MIN_TERMINAL_WIDTH}x{MIN_TERMINAL_HEIGHT}, "
                f"got {self.term.width}x{self.term.height}"
            )
        return True, ""

    def clear(self) -> None:
        """Clear the entire screen."""
        self._buffer.append(self.term.clear)

    def move(self, x: int, y: int) -> None:
        """Move cursor to position.

        Args:
            x: Column position (0-indexed)
            y: Row position (0-indexed)
        """
        self._buffer.append(self.term.move_xy(x, y))

    def write(self, text: str, color: Optional[str] = None) -> None:
        """Write text at current cursor position.

        Args:
            text: Text to write
            color: Optional color name (blessed color)
        """
        if color:
            colored_text = getattr(self.term, color)(text)
            self._buffer.append(colored_text)
        else:
            self._buffer.append(text)

    def write_at(self, x: int, y: int, text: str, color: Optional[str] = None) -> None:
        """Write text at specific position, automatically centered.

        Args:
            x: Column position (game coordinates, will be centered)
            y: Row position
            text: Text to write
            color: Optional color name
        """
        adjusted_x = x + self.x_offset
        self.move(adjusted_x, y)
        self.write(text, color)

    def flush(self) -> None:
        """Flush buffer to terminal."""
        if self._buffer:
            print("".join(self._buffer), end="", flush=True)
            self._buffer.clear()

    def inkey(self, timeout: float = 0) -> Any:
        """Read a keystroke with optional timeout.

        Args:
            timeout: Timeout in seconds (0 for non-blocking)

        Returns:
            Keystroke object or empty string if no input
        """
        return self.term.inkey(timeout=timeout)

    def hide_cursor(self) -> str:
        """Return sequence to hide cursor."""
        return self.term.hide_cursor

    def show_cursor(self) -> str:
        """Return sequence to show cursor."""
        return self.term.normal_cursor

    def fullscreen(self) -> Any:
        """Return context manager for fullscreen mode."""
        return self.term.fullscreen()

    def cbreak(self) -> Any:
        """Return context manager for cbreak mode (no line buffering)."""
        return self.term.cbreak()

    def hidden_cursor(self) -> Any:
        """Return context manager for hidden cursor."""
        return self.term.hidden_cursor()

    @property
    def width(self) -> int:
        """Get terminal width."""
        return self.term.width

    @property
    def height(self) -> int:
        """Get terminal height."""
        return self.term.height

    def get_color(self, color_name: str) -> Any:
        """Get blessed color formatter.

        Args:
            color_name: Name of the color

        Returns:
            Blessed color formatter
        """
        return getattr(self.term, color_name, self.term.normal)
