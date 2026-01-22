"""Visual effects like explosions and particles."""
from typing import List

from ..config import COLOR_EXPLOSION
from ..renderer.sprites import EXPLOSION_FRAMES


class Explosion:
    """Explosion animation effect."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize explosion.

        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.frame = 0
        self.frames = EXPLOSION_FRAMES
        self.frame_time = 0.0
        self.frame_duration = 0.1  # Seconds per frame
        self.alive = True
        self.color = COLOR_EXPLOSION

    def update(self, dt: float) -> None:
        """Update explosion animation.

        Args:
            dt: Delta time in seconds
        """
        self.frame_time += dt

        if self.frame_time >= self.frame_duration:
            self.frame_time = 0.0
            self.frame += 1

            if self.frame >= len(self.frames):
                self.alive = False

    def get_sprite(self) -> List[str]:
        """Get current animation frame.

        Returns:
            List of sprite lines for current frame
        """
        if self.frame < len(self.frames):
            return self.frames[self.frame]
        return []


class EffectsManager:
    """Manages visual effects."""

    def __init__(self) -> None:
        """Initialize effects manager."""
        self.explosions: List[Explosion] = []

    def add_explosion(self, x: int, y: int) -> None:
        """Add an explosion effect.

        Args:
            x: X position
            y: Y position
        """
        self.explosions.append(Explosion(x, y))

    def update(self, dt: float) -> None:
        """Update all effects.

        Args:
            dt: Delta time in seconds
        """
        for explosion in self.explosions:
            explosion.update(dt)

        # Remove dead explosions
        self.explosions = [e for e in self.explosions if e.alive]

    def clear(self) -> None:
        """Clear all effects."""
        self.explosions.clear()
