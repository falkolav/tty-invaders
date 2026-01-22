"""Scoring system."""
from typing import Optional


class ScoreManager:
    """Manages game scoring."""

    def __init__(self) -> None:
        """Initialize score manager."""
        self.score = 0
        self.high_score = 0

    def add_score(self, points: int) -> None:
        """Add points to the score.

        Args:
            points: Points to add
        """
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self) -> None:
        """Reset score for new game."""
        self.score = 0

    def load_high_score(self, high_score: int) -> None:
        """Load high score from persistence.

        Args:
            high_score: High score value
        """
        self.high_score = max(self.high_score, high_score)

    def is_high_score(self) -> bool:
        """Check if current score is a high score.

        Returns:
            True if current score equals high score
        """
        return self.score > 0 and self.score >= self.high_score
