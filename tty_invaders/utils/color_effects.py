"""Color effects manager for visual modes."""
import time
import random


class ColorEffects:
    """Manages visual color effects for different game modes."""

    # Available blessed colors
    COLORS = [
        "red", "green", "yellow", "blue", "magenta", "cyan",
        "bright_red", "bright_green", "bright_yellow",
        "bright_blue", "bright_magenta", "bright_cyan"
    ]

    RAINBOW_COLORS = [
        "red", "bright_red", "yellow", "bright_yellow",
        "green", "bright_green", "cyan", "bright_cyan",
        "blue", "bright_blue", "magenta", "bright_magenta"
    ]

    MATRIX_COLORS = ["green", "bright_green"]
    PSYCHEDELIC_COLORS = [
        "bright_magenta", "bright_cyan", "bright_yellow",
        "bright_red", "bright_blue", "bright_green"
    ]

    def __init__(self, mode: str = "normal") -> None:
        """Initialize color effects.

        Args:
            mode: Color mode (normal, rainbow, disco, matrix, psychedelic)
        """
        self.mode = mode
        self.frame = 0
        self.start_time = time.time()

    def set_mode(self, mode: str) -> None:
        """Set the color mode.

        Args:
            mode: Color mode name
        """
        self.mode = mode

    def update(self) -> None:
        """Update color effects (call once per frame)."""
        self.frame += 1

    def get_color(self, original_color: str, entity_id: int = 0) -> str:
        """Get the modified color based on current mode.

        Args:
            original_color: Original color name
            entity_id: Unique ID for the entity (for consistent rainbow mapping)

        Returns:
            Modified color name
        """
        if self.mode == "normal":
            return original_color

        elif self.mode == "rainbow":
            # Cycle through rainbow colors
            color_index = (self.frame // 3 + entity_id) % len(self.RAINBOW_COLORS)
            return self.RAINBOW_COLORS[color_index]

        elif self.mode == "disco":
            # Rapid random flashing
            if self.frame % 2 == 0:
                return random.choice(self.COLORS)
            return original_color

        elif self.mode == "matrix":
            # Green Matrix theme
            return random.choice(self.MATRIX_COLORS)

        elif self.mode == "psychedelic":
            # Intense color cycling
            color_index = (self.frame // 2 + entity_id * 3) % len(self.PSYCHEDELIC_COLORS)
            return self.PSYCHEDELIC_COLORS[color_index]

        return original_color

    def get_player_color(self, original_color: str) -> str:
        """Get player color with effects.

        Args:
            original_color: Original player color

        Returns:
            Modified color
        """
        return self.get_color(original_color, 999)

    def get_alien_color(self, original_color: str, alien_id: int) -> str:
        """Get alien color with effects.

        Args:
            original_color: Original alien color
            alien_id: Alien identifier

        Returns:
            Modified color
        """
        return self.get_color(original_color, alien_id)

    def get_bullet_color(self, original_color: str, is_player: bool) -> str:
        """Get bullet color with effects.

        Args:
            original_color: Original bullet color
            is_player: Whether this is a player bullet

        Returns:
            Modified color
        """
        entity_id = 1000 if is_player else 2000
        return self.get_color(original_color, entity_id)

    def get_ui_color(self, original_color: str) -> str:
        """Get UI color (usually keep normal).

        Args:
            original_color: Original UI color

        Returns:
            Modified color
        """
        if self.mode == "matrix":
            return "bright_green"
        elif self.mode == "psychedelic":
            return self.get_color(original_color, 0)
        return original_color
