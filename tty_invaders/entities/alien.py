"""Alien entity."""
from typing import List, Optional

from ..config import COLOR_ALIEN_TOP, COLOR_ALIEN_MID, COLOR_ALIEN_BOT
from ..renderer.sprites import get_alien_sprite, get_sprite_width


class Alien:
    """Alien entity."""

    def __init__(self, x: int, y: int, row: int, col: int) -> None:
        """Initialize alien.

        Args:
            x: X position
            y: Y position
            row: Row in formation (0-indexed from top)
            col: Column in formation
        """
        self.x = float(x)
        self.y = y
        self.row = row
        self.col = col
        self.alive = True
        self.animated = False

        # Set sprite and color based on row
        self.sprite = get_alien_sprite(row, self.animated)
        self.width = get_sprite_width(self.sprite)
        self.height = len(self.sprite)

        # Color based on row
        if row == 0:
            self.color = COLOR_ALIEN_TOP
        elif row <= 2:
            self.color = COLOR_ALIEN_MID
        else:
            self.color = COLOR_ALIEN_BOT

    def update_animation(self, animated: bool) -> None:
        """Update animation frame.

        Args:
            animated: Whether to show alternate animation frame
        """
        if self.animated != animated:
            self.animated = animated
            self.sprite = get_alien_sprite(self.row, self.animated)

    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get bounding box for collision detection.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (int(self.x), self.y, self.width, self.height)

    def get_score_value(self) -> int:
        """Get point value for destroying this alien.

        Returns:
            Score points
        """
        from ..config import SCORE_ALIEN_TOP, SCORE_ALIEN_MID, SCORE_ALIEN_BOT

        if self.row == 0:
            return SCORE_ALIEN_TOP
        elif self.row <= 2:
            return SCORE_ALIEN_MID
        else:
            return SCORE_ALIEN_BOT
