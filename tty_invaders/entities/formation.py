"""Alien formation manager."""
import random
from typing import List, Optional

from .alien import Alien
from .bullet import Bullet
from ..config import (
    ALIEN_COLS, ALIEN_ROWS, ALIEN_SPACING_X, ALIEN_SPACING_Y,
    ALIEN_START_X, ALIEN_START_Y, ALIEN_BASE_SPEED, ALIEN_SPEED_INCREMENT,
    ALIEN_DESCENT, GAME_WIDTH, ALIEN_BASE_SHOOT_FREQ, ALIEN_SHOOT_FREQ_DECREMENT,
    MIN_SHOOT_FREQUENCY, MAX_ALIEN_ROWS
)


class AlienFormation:
    """Manages the alien formation."""

    def __init__(self, level: int = 1) -> None:
        """Initialize formation.

        Args:
            level: Current game level
        """
        self.level = level
        self.aliens: List[Alien] = []
        self.direction = 1  # 1 = right, -1 = left
        self.speed = ALIEN_BASE_SPEED + (level - 1) * ALIEN_SPEED_INCREMENT
        self.shoot_timer = 0.0
        self.shoot_frequency = max(
            MIN_SHOOT_FREQUENCY,
            ALIEN_BASE_SHOOT_FREQ - (level - 1) * ALIEN_SHOOT_FREQ_DECREMENT
        )
        self.animation_timer = 0.0
        self.animation_state = False

        # Calculate rows for this level
        self.rows = min(ALIEN_ROWS + (level - 1) // 2, MAX_ALIEN_ROWS)

        self._create_formation()

    def _create_formation(self) -> None:
        """Create the initial alien formation."""
        self.aliens.clear()

        for row in range(self.rows):
            for col in range(ALIEN_COLS):
                x = ALIEN_START_X + col * ALIEN_SPACING_X
                y = ALIEN_START_Y + row * ALIEN_SPACING_Y
                alien = Alien(x, y, row, col)
                self.aliens.append(alien)

    def update(self, dt: float) -> None:
        """Update formation position and state.

        Args:
            dt: Delta time in seconds
        """
        if not self.aliens:
            return

        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= 0.5:  # Toggle every 0.5 seconds
            self.animation_timer = 0.0
            self.animation_state = not self.animation_state
            for alien in self.aliens:
                if alien.alive:
                    alien.update_animation(self.animation_state)

        # Move formation
        move_amount = self.speed * dt * self.direction

        # Check if any alien hit the edge
        should_descend = False
        for alien in self.aliens:
            if not alien.alive:
                continue

            new_x = alien.x + move_amount
            if new_x < 0 or new_x + alien.width >= GAME_WIDTH:
                should_descend = True
                break

        if should_descend:
            # Reverse direction and descend
            self.direction *= -1
            for alien in self.aliens:
                if alien.alive:
                    alien.y += ALIEN_DESCENT
        else:
            # Normal horizontal movement
            for alien in self.aliens:
                if alien.alive:
                    alien.x += move_amount

        # Update shoot timer
        self.shoot_timer += dt

    def try_shoot(self) -> Optional[Bullet]:
        """Attempt to make a random alien shoot.

        Returns:
            Bullet instance if successful, None otherwise
        """
        if self.shoot_timer < self.shoot_frequency:
            return None

        # Reset timer
        self.shoot_timer = 0.0

        # Get alive aliens
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens:
            return None

        # Choose random alien
        shooter = random.choice(alive_aliens)

        # Create bullet from center bottom of alien
        bullet_x = int(shooter.x + shooter.width // 2)
        bullet_y = shooter.y + shooter.height
        return Bullet(bullet_x, bullet_y, is_player=False)

    def get_alive_aliens(self) -> List[Alien]:
        """Get list of alive aliens.

        Returns:
            List of alive Alien instances
        """
        return [a for a in self.aliens if a.alive]

    def is_cleared(self) -> bool:
        """Check if all aliens are destroyed.

        Returns:
            True if no aliens remain
        """
        return len(self.get_alive_aliens()) == 0

    def get_lowest_y(self) -> int:
        """Get the Y position of the lowest alien.

        Returns:
            Lowest Y position, or 0 if no aliens
        """
        alive = self.get_alive_aliens()
        if not alive:
            return 0
        return max(a.y + a.height for a in alive)

    def reset(self, level: int) -> None:
        """Reset formation for new level.

        Args:
            level: New level number
        """
        self.level = level
        self.direction = 1
        self.speed = ALIEN_BASE_SPEED + (level - 1) * ALIEN_SPEED_INCREMENT
        self.shoot_frequency = max(
            MIN_SHOOT_FREQUENCY,
            ALIEN_BASE_SHOOT_FREQ - (level - 1) * ALIEN_SHOOT_FREQ_DECREMENT
        )
        self.shoot_timer = 0.0
        self.animation_timer = 0.0
        self.animation_state = False
        self.rows = min(ALIEN_ROWS + (level - 1) // 2, MAX_ALIEN_ROWS)
        self._create_formation()
