"""Shield entity."""
from typing import List

from ..config import (
    SHIELD_WIDTH, SHIELD_HEIGHT, SHIELD_HEALTH, SHIELD_Y,
    GAME_WIDTH, SHIELD_COUNT, COLOR_SHIELD
)
from ..renderer.sprites import get_shield_sprite


class Shield:
    """Destructible shield."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize shield.

        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.width = SHIELD_WIDTH
        self.height = SHIELD_HEIGHT
        self.health = SHIELD_HEALTH
        self.max_health = SHIELD_HEALTH
        self.alive = True
        self.color = COLOR_SHIELD

    def take_damage(self, amount: int = 1) -> None:
        """Take damage to the shield.

        Args:
            amount: Amount of damage to take
        """
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def get_health_percent(self) -> float:
        """Get health as a percentage.

        Returns:
            Health percentage (0.0 - 1.0)
        """
        return self.health / self.max_health

    def get_sprite(self) -> List[str]:
        """Get current shield sprite based on health.

        Returns:
            List of sprite lines
        """
        return get_shield_sprite(self.get_health_percent())

    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get bounding box for collision detection.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)


def create_shields() -> List[Shield]:
    """Create the standard set of shields.

    Returns:
        List of Shield instances
    """
    shields = []
    spacing = GAME_WIDTH // (SHIELD_COUNT + 1)

    for i in range(SHIELD_COUNT):
        x = spacing * (i + 1) - SHIELD_WIDTH // 2
        shield = Shield(x, SHIELD_Y)
        shields.append(shield)

    return shields
