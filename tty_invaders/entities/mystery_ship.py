"""Mystery ship (UFO) entity."""
from typing import Tuple
from ..config import GAME_WIDTH, PLAY_AREA_TOP


# Mystery ship sprite
MYSTERY_SHIP_SPRITE = [
    " <-O-> "
]


class MysteryShip:
    """Mystery ship that flies across the screen."""

    def __init__(self, direction: int = 1) -> None:
        """Initialize mystery ship.

        Args:
            direction: 1 for left-to-right, -1 for right-to-left
        """
        self.direction = direction
        self.alive = True
        self.sprite = MYSTERY_SHIP_SPRITE
        self.width = len(self.sprite[0])
        self.height = len(self.sprite)
        self.color = "red"
        self.speed = 15  # Characters per second
        self.y = PLAY_AREA_TOP

        # Start position based on direction
        if direction > 0:
            self.x = float(-self.width)  # Start off-screen left
        else:
            self.x = float(GAME_WIDTH)  # Start off-screen right

        self.score_value = 0  # Will be set based on shot count

    def update(self, dt: float) -> None:
        """Update mystery ship position.

        Args:
            dt: Delta time in seconds
        """
        self.x += self.direction * self.speed * dt

        # Check if off screen
        if self.direction > 0:
            if self.x > GAME_WIDTH + 5:
                self.alive = False
        else:
            if self.x < -self.width - 5:
                self.alive = False

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Get bounding box for collision detection.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (int(self.x), self.y, self.width, self.height)

    def get_position(self) -> Tuple[int, int]:
        """Get mystery ship position for rendering.

        Returns:
            Tuple of (x, y)
        """
        return (int(self.x), self.y)

    def set_score_value(self, value: int) -> None:
        """Set the score value for this mystery ship.

        Args:
            value: Score value (50, 100, 150, or 300)
        """
        self.score_value = value
