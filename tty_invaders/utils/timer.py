"""Frame timing utilities."""
import time
from typing import Optional


class GameTimer:
    """Manages frame timing and delta time calculation."""

    def __init__(self, target_fps: int = 60) -> None:
        """Initialize the timer.

        Args:
            target_fps: Target frames per second
        """
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.last_time: Optional[float] = None
        self.delta_time: float = 0.0

    def tick(self) -> float:
        """Calculate delta time since last tick.

        Returns:
            Delta time in seconds
        """
        current_time = time.time()

        if self.last_time is None:
            self.delta_time = self.frame_time
        else:
            self.delta_time = current_time - self.last_time

        self.last_time = current_time
        return self.delta_time

    def wait_for_next_frame(self) -> None:
        """Sleep until next frame is due."""
        if self.last_time is None:
            return

        elapsed = time.time() - self.last_time
        sleep_time = self.frame_time - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)
