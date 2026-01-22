"""Bullet entity."""
from ..config import (
    BULLET_SPEED, PLAY_AREA_TOP, PLAY_AREA_BOTTOM,
    COLOR_BULLET_PLAYER, COLOR_BULLET_ALIEN,
    PLAYER_BULLET_CHAR, ALIEN_BULLET_CHAR
)


class Bullet:
    """Bullet entity."""

    def __init__(self, x: int, y: int, is_player: bool = True) -> None:
        """Initialize bullet.

        Args:
            x: X position
            y: Y position
            is_player: True if fired by player, False if fired by alien
        """
        self.x = x
        self.y = float(y)
        self.is_player = is_player
        self.alive = True
        self.speed = BULLET_SPEED

        if is_player:
            self.direction = -1  # Move up
            self.char = PLAYER_BULLET_CHAR
            self.color = COLOR_BULLET_PLAYER
        else:
            self.direction = 1  # Move down
            self.char = ALIEN_BULLET_CHAR
            self.color = COLOR_BULLET_ALIEN

    def update(self, dt: float) -> None:
        """Update bullet position.

        Args:
            dt: Delta time in seconds
        """
        self.y += self.direction * self.speed * dt

        # Check if bullet is out of bounds
        if self.direction < 0:  # Player bullet moving up
            if self.y < PLAY_AREA_TOP:
                self.alive = False
        else:  # Alien bullet moving down
            if self.y > PLAY_AREA_BOTTOM:
                self.alive = False

    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get bounding box for collision detection.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (self.x, int(self.y), 1, 1)

    def get_position(self) -> tuple[int, int]:
        """Get bullet position for rendering.

        Returns:
            Tuple of (x, y)
        """
        return (self.x, int(self.y))
