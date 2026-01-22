"""Tests for persistence system."""
import os
import tempfile
import pytest
from tty_invaders.utils.persistence import HighScoreEntry, HighScoreManager


class TestHighScoreEntry:
    """Test high score entry."""

    def test_create_entry(self) -> None:
        """Test creating a high score entry."""
        entry = HighScoreEntry("ABC", 1000, 5)
        assert entry.name == "ABC"
        assert entry.score == 1000
        assert entry.level == 5
        assert entry.date != ""

    def test_to_dict(self) -> None:
        """Test converting entry to dictionary."""
        entry = HighScoreEntry("XYZ", 2000, 10, "2024-01-01")
        data = entry.to_dict()
        assert data["name"] == "XYZ"
        assert data["score"] == 2000
        assert data["level"] == 10
        assert data["date"] == "2024-01-01"

    def test_from_dict(self) -> None:
        """Test creating entry from dictionary."""
        data = {"name": "AAA", "score": 500, "level": 3, "date": "2024-01-01"}
        entry = HighScoreEntry.from_dict(data)
        assert entry.name == "AAA"
        assert entry.score == 500
        assert entry.level == 3
        assert entry.date == "2024-01-01"


class TestHighScoreManager:
    """Test high score manager."""

    def test_empty_high_scores(self) -> None:
        """Test manager with no high scores."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            manager = HighScoreManager(temp_file)
            assert len(manager.get_entries()) == 0
            assert manager.get_top_score() == 0
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_add_score(self) -> None:
        """Test adding a high score."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            manager = HighScoreManager(temp_file)
            position = manager.add_score("ABC", 1000, 5)
            assert position == 1
            assert len(manager.get_entries()) == 1
            assert manager.get_top_score() == 1000
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_add_multiple_scores(self) -> None:
        """Test adding multiple scores."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            manager = HighScoreManager(temp_file)
            manager.add_score("AAA", 500, 3)
            manager.add_score("BBB", 1000, 5)
            manager.add_score("CCC", 750, 4)

            entries = manager.get_entries()
            assert len(entries) == 3
            # Should be sorted by score
            assert entries[0].score == 1000
            assert entries[1].score == 750
            assert entries[2].score == 500
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_max_high_scores(self) -> None:
        """Test that only top 10 scores are kept."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            manager = HighScoreManager(temp_file)
            # Add 15 scores
            for i in range(15):
                manager.add_score("AAA", i * 100, 1)

            entries = manager.get_entries()
            assert len(entries) == 10
            # Highest score should be 1400
            assert entries[0].score == 1400
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_is_high_score(self) -> None:
        """Test checking if a score qualifies."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            manager = HighScoreManager(temp_file)

            # Empty list - any score qualifies
            assert manager.is_high_score(100)

            # Add 10 scores
            for i in range(10):
                manager.add_score("AAA", (i + 1) * 100, 1)

            # Higher than lowest should qualify
            assert manager.is_high_score(150)

            # Lower than lowest should not qualify
            assert not manager.is_high_score(50)

            # Equal to highest should qualify
            assert manager.is_high_score(1000)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_persistence(self) -> None:
        """Test that scores persist across instances."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            # Create first manager and add score
            manager1 = HighScoreManager(temp_file)
            manager1.add_score("ABC", 1000, 5)

            # Create second manager - should load the score
            manager2 = HighScoreManager(temp_file)
            assert len(manager2.get_entries()) == 1
            assert manager2.get_top_score() == 1000
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
