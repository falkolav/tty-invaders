"""Player entity."""
from typing import List, Optional

from ..config import (
    PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN,
    GAME_WIDTH, PLAY_AREA_BOTTOM, COLOR_PLAYER
)
from ..renderer.sprites import PLAYER_SPRITE, get_sprite_width


class Player:
    """Player entity."""

    def __init__(self) -> None:
        """Initialize player."""
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.sprite = PLAYER_SPRITE
        self.width = get_sprite_width(self.sprite)
        self.height = len(self.sprite)
        self.alive = True
        self.shoot_cooldown = 0.0
        self.color = COLOR_PLAYER
        self.speed = PLAYER_SPEED

    def move_left(self, dt: float) -> None:
        """Move player left.

        Args:
            dt: Delta time in seconds
        """
        self.x -= self.speed * dt
        self.x = max(0, self.x)

    def move_right(self, dt: float) -> None:
        """Move player right.

        Args:
            dt: Delta time in seconds
        """
        self.x += self.speed * dt
        self.x = min(GAME_WIDTH - self.width, self.x)

    def can_shoot(self) -> bool:
        """Check if player can shoot.

        Returns:
            True if cooldown has expired
        """
        return self.shoot_cooldown <= 0

    def shoot(self) -> Optional['Bullet']:
        """Attempt to shoot a bullet.

        Returns:
            Bullet instance if successful, None otherwise
        """
        if not self.can_shoot():
            return None

        from .bullet import Bullet

        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        # Shoot from center of player
        bullet_x = int(self.x + self.width // 2)
        bullet_y = self.y - 1
        return Bullet(bullet_x, bullet_y, is_player=True)

    def create_bullet(self) -> Optional['Bullet']:
        """Create a bullet without checking cooldown (for rapid fire mode).

        Returns:
            Bullet instance
        """
        from .bullet import Bullet

        # Shoot from center of player
        bullet_x = int(self.x + self.width // 2)
        bullet_y = self.y - 1
        return Bullet(bullet_x, bullet_y, is_player=True)

    def update(self, dt: float) -> None:
        """Update player state.

        Args:
            dt: Delta time in seconds
        """
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get bounding box for collision detection.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (int(self.x), self.y, self.width, self.height)

    def reset(self) -> None:
        """Reset player to starting position."""
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.alive = True
        self.shoot_cooldown = 0.0
        self.speed = PLAYER_SPEED
