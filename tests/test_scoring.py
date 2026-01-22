"""Tests for scoring system."""
import pytest
from tty_invaders.systems.scoring import ScoreManager


class TestScoreManager:
    """Test score management."""

    def test_initial_score(self) -> None:
        """Test initial score is zero."""
        manager = ScoreManager()
        assert manager.score == 0
        assert manager.high_score == 0

    def test_add_score(self) -> None:
        """Test adding score."""
        manager = ScoreManager()
        manager.add_score(100)
        assert manager.score == 100

    def test_add_multiple_scores(self) -> None:
        """Test adding multiple scores."""
        manager = ScoreManager()
        manager.add_score(100)
        manager.add_score(50)
        manager.add_score(25)
        assert manager.score == 175

    def test_high_score_updates(self) -> None:
        """Test high score updates when score exceeds it."""
        manager = ScoreManager()
        manager.add_score(100)
        assert manager.high_score == 100

        manager.add_score(50)
        assert manager.high_score == 150

    def test_reset_score(self) -> None:
        """Test resetting score."""
        manager = ScoreManager()
        manager.add_score(100)
        manager.reset()
        assert manager.score == 0
        # High score should not be reset
        assert manager.high_score == 100

    def test_load_high_score(self) -> None:
        """Test loading high score."""
        manager = ScoreManager()
        manager.load_high_score(500)
        assert manager.high_score == 500

    def test_load_lower_high_score(self) -> None:
        """Test loading high score lower than current."""
        manager = ScoreManager()
        manager.add_score(600)
        manager.load_high_score(500)
        # Should keep higher score
        assert manager.high_score == 600

    def test_is_high_score(self) -> None:
        """Test checking if current score is high score."""
        manager = ScoreManager()
        assert not manager.is_high_score()  # Zero score is not high score

        manager.add_score(100)
        assert manager.is_high_score()

        manager.reset()
        manager.load_high_score(200)
        manager.add_score(150)
        assert not manager.is_high_score()

        manager.add_score(50)  # Now at 200
        assert manager.is_high_score()
