"""Tests for collision detection system."""
import pytest
from tty_invaders.systems.collision import check_aabb_collision


class TestAABBCollision:
    """Test AABB collision detection."""

    def test_no_collision(self) -> None:
        """Test boxes that don't overlap."""
        box1 = (0, 0, 5, 5)
        box2 = (10, 10, 5, 5)
        assert not check_aabb_collision(box1, box2)

    def test_collision_overlap(self) -> None:
        """Test boxes that overlap."""
        box1 = (0, 0, 5, 5)
        box2 = (3, 3, 5, 5)
        assert check_aabb_collision(box1, box2)

    def test_collision_edge_touching(self) -> None:
        """Test boxes that touch at edge."""
        box1 = (0, 0, 5, 5)
        box2 = (5, 0, 5, 5)
        # Edge touching should not be considered collision
        assert not check_aabb_collision(box1, box2)

    def test_collision_contained(self) -> None:
        """Test box completely inside another."""
        box1 = (0, 0, 10, 10)
        box2 = (2, 2, 3, 3)
        assert check_aabb_collision(box1, box2)

    def test_collision_same_position(self) -> None:
        """Test boxes at same position."""
        box1 = (5, 5, 3, 3)
        box2 = (5, 5, 3, 3)
        assert check_aabb_collision(box1, box2)

    def test_collision_vertical_overlap_only(self) -> None:
        """Test boxes that overlap vertically but not horizontally."""
        box1 = (0, 0, 5, 10)
        box2 = (10, 2, 5, 5)
        assert not check_aabb_collision(box1, box2)

    def test_collision_horizontal_overlap_only(self) -> None:
        """Test boxes that overlap horizontally but not vertically."""
        box1 = (0, 0, 10, 5)
        box2 = (2, 10, 5, 5)
        assert not check_aabb_collision(box1, box2)
