"""Tests for game entities."""
import pytest
from tty_invaders.entities.player import Player
from tty_invaders.entities.bullet import Bullet
from tty_invaders.entities.alien import Alien
from tty_invaders.config import PLAYER_START_X, PLAYER_START_Y, GAME_WIDTH


class TestPlayer:
    """Test player entity."""

    def test_player_initialization(self) -> None:
        """Test player starts at correct position."""
        player = Player()
        assert player.x == PLAYER_START_X
        assert player.y == PLAYER_START_Y
        assert player.alive is True

    def test_player_move_left(self) -> None:
        """Test player moves left."""
        player = Player()
        initial_x = player.x
        player.move_left(0.1)  # Delta time of 0.1 seconds
        assert player.x < initial_x

    def test_player_move_right(self) -> None:
        """Test player moves right."""
        player = Player()
        initial_x = player.x
        player.move_right(0.1)
        assert player.x > initial_x

    def test_player_boundary_left(self) -> None:
        """Test player can't move past left boundary."""
        player = Player()
        player.x = 0
        player.move_left(1.0)
        assert player.x == 0

    def test_player_boundary_right(self) -> None:
        """Test player can't move past right boundary."""
        player = Player()
        player.x = GAME_WIDTH - player.width
        player.move_right(1.0)
        assert player.x == GAME_WIDTH - player.width

    def test_player_shoot_cooldown(self) -> None:
        """Test player shooting has cooldown."""
        player = Player()
        bullet1 = player.shoot()
        assert bullet1 is not None

        # Immediate second shot should fail
        bullet2 = player.shoot()
        assert bullet2 is None

        # After updating cooldown, should be able to shoot
        player.update(1.0)  # 1 second should be enough
        bullet3 = player.shoot()
        assert bullet3 is not None

    def test_player_reset(self) -> None:
        """Test player reset."""
        player = Player()
        player.x = 50
        player.alive = False
        player.reset()
        assert player.x == PLAYER_START_X
        assert player.y == PLAYER_START_Y
        assert player.alive is True


class TestBullet:
    """Test bullet entity."""

    def test_player_bullet_initialization(self) -> None:
        """Test player bullet initialization."""
        bullet = Bullet(10, 15, is_player=True)
        assert bullet.x == 10
        assert bullet.y == 15
        assert bullet.is_player is True
        assert bullet.alive is True
        assert bullet.direction == -1  # Player bullets go up

    def test_alien_bullet_initialization(self) -> None:
        """Test alien bullet initialization."""
        bullet = Bullet(10, 15, is_player=False)
        assert bullet.is_player is False
        assert bullet.direction == 1  # Alien bullets go down

    def test_bullet_movement(self) -> None:
        """Test bullet moves in correct direction."""
        player_bullet = Bullet(10, 15, is_player=True)
        initial_y = player_bullet.y
        player_bullet.update(0.1)
        assert player_bullet.y < initial_y  # Moved up

        alien_bullet = Bullet(10, 15, is_player=False)
        initial_y = alien_bullet.y
        alien_bullet.update(0.1)
        assert alien_bullet.y > initial_y  # Moved down

    def test_bullet_bounds(self) -> None:
        """Test bullet bounds for collision."""
        bullet = Bullet(10, 15)
        x, y, w, h = bullet.get_bounds()
        assert x == 10
        assert y == 15
        assert w == 1
        assert h == 1


class TestAlien:
    """Test alien entity."""

    def test_alien_initialization(self) -> None:
        """Test alien initialization."""
        alien = Alien(10, 5, row=0, col=0)
        assert alien.x == 10
        assert alien.y == 5
        assert alien.row == 0
        assert alien.col == 0
        assert alien.alive is True

    def test_alien_score_values(self) -> None:
        """Test different aliens have different scores."""
        alien_top = Alien(0, 0, row=0, col=0)
        alien_mid = Alien(0, 0, row=2, col=0)
        alien_bot = Alien(0, 0, row=4, col=0)

        assert alien_top.get_score_value() > alien_mid.get_score_value()
        assert alien_mid.get_score_value() > alien_bot.get_score_value()

    def test_alien_animation(self) -> None:
        """Test alien animation toggle."""
        alien = Alien(0, 0, row=0, col=0)
        initial_sprite = alien.sprite

        alien.update_animation(True)
        assert alien.sprite != initial_sprite

        alien.update_animation(False)
        assert alien.sprite == initial_sprite
