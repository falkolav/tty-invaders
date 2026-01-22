"""High score persistence."""
import json
import os
from typing import List, Dict, Any
from datetime import datetime

from ..config import HIGH_SCORE_FILE, MAX_HIGH_SCORES


class HighScoreEntry:
    """High score entry."""

    def __init__(self, name: str, score: int, level: int, date: str = "", game_mode: str = "normal") -> None:
        """Initialize high score entry.

        Args:
            name: Player name (3 characters)
            score: Score achieved
            level: Level reached
            date: Date string (ISO format)
            game_mode: Game mode used (normal, turbo, etc.)
        """
        self.name = name
        self.score = score
        self.level = level
        self.date = date or datetime.now().isoformat()
        self.game_mode = game_mode

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "score": self.score,
            "level": self.level,
            "date": self.date,
            "game_mode": self.game_mode
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HighScoreEntry':
        """Create from dictionary.

        Args:
            data: Dictionary with entry data

        Returns:
            HighScoreEntry instance
        """
        return cls(
            name=data.get("name", "AAA"),
            score=data.get("score", 0),
            level=data.get("level", 1),
            date=data.get("date", ""),
            game_mode=data.get("game_mode", "normal")
        )


class HighScoreManager:
    """Manages high score persistence."""

    def __init__(self, filename: str = HIGH_SCORE_FILE) -> None:
        """Initialize high score manager.

        Args:
            filename: Path to high score file
        """
        self.filename = filename
        self.entries: List[HighScoreEntry] = []
        self.load()

    def load(self) -> None:
        """Load high scores from file."""
        if not os.path.exists(self.filename):
            self.entries = []
            return

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.entries = [HighScoreEntry.from_dict(entry) for entry in data]
        except (json.JSONDecodeError, IOError):
            self.entries = []

    def save(self) -> None:
        """Save high scores to file."""
        try:
            with open(self.filename, 'w') as f:
                data = [entry.to_dict() for entry in self.entries]
                json.dump(data, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't save

    def add_score(self, name: str, score: int, level: int, game_mode: str = "normal") -> int:
        """Add a new high score.

        Args:
            name: Player name
            score: Score achieved
            level: Level reached
            game_mode: Game mode used

        Returns:
            Position in high score table (1-indexed), or 0 if not in top scores
        """
        entry = HighScoreEntry(name, score, level, game_mode=game_mode)
        self.entries.append(entry)

        # Sort by score (descending)
        self.entries.sort(key=lambda e: e.score, reverse=True)

        # Keep only top entries
        self.entries = self.entries[:MAX_HIGH_SCORES]

        # Save to file
        self.save()

        # Return position (1-indexed)
        try:
            return self.entries.index(entry) + 1
        except ValueError:
            return 0

    def is_high_score(self, score: int) -> bool:
        """Check if a score qualifies as a high score.

        Args:
            score: Score to check

        Returns:
            True if score would be in top scores
        """
        if len(self.entries) < MAX_HIGH_SCORES:
            return True

        return score > self.entries[-1].score

    def get_top_score(self) -> int:
        """Get the highest score.

        Returns:
            Highest score, or 0 if no scores
        """
        if self.entries:
            return self.entries[0].score
        return 0

    def get_entries(self) -> List[HighScoreEntry]:
        """Get all high score entries.

        Returns:
            List of high score entries
        """
        return self.entries.copy()
