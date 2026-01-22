"""Playing state - main gameplay."""
from typing import Any, List

from .base import BaseState
from ..renderer.terminal import Terminal
from ..renderer.ui import render_ui
from ..renderer.effects import EffectsManager
from ..entities.player import Player
from ..entities.bullet import Bullet
from ..entities.formation import AlienFormation
from ..entities.shield import Shield, create_shields
from ..entities.mystery_ship import MysteryShip
from ..systems.input import InputState, process_gameplay_input
from ..utils.color_effects import ColorEffects
from ..systems.collision import (
    check_bullet_alien_collisions, check_bullet_shield_collisions,
    check_bullet_player_collision, check_alien_player_collision,
    check_aliens_reached_bottom
)
from ..config import PLAYER_LIVES, PLAY_AREA_BOTTOM


class PlayingState(BaseState):
    """Main gameplay state."""

    def __init__(self, game: Any) -> None:
        """Initialize playing state.

        Args:
            game: Reference to the main game instance
        """
        super().__init__(game)
        self.sound_manager = game.sound_manager
        self.player = Player()
        self.formation = AlienFormation(1)
        self.shields: List[Shield] = []
        self.bullets: List[Bullet] = []
        self.input_state = InputState()
        self.effects = EffectsManager()
        self.settings = None
        self.frame_count = 0
        self.color_effects = ColorEffects()
        self.mystery_ship = None
        self.mystery_ship_timer = 0.0
        self.mystery_ship_interval = 25.0  # Appears every ~25 seconds
        self.shot_count = 0  # Track shots for 300pt mystery ship
        self.last_heartbeat_time = 0.0

    def enter(self) -> None:
        """Called when entering playing state."""
        # Load settings
        from ..utils.settings import GameSettings
        self.settings = GameSettings()

        # Reset game state
        self.game.reset_game()

        # Initialize entities
        self.player.reset()
        self.formation.reset(self.game.level)
        self.shields = create_shields()
        self.bullets.clear()
        self.effects.clear()
        self.frame_count = 0

        # Apply speed multipliers to player
        player_mult, alien_mult, bullet_mult = self.settings.get_speed_multipliers()
        self.player.speed *= player_mult

        # Set color mode
        color_mode = self.settings.get("color_mode", "normal")
        self.color_effects.set_mode(color_mode)

        # Reset mystery ship tracking
        self.mystery_ship = None
        self.mystery_ship_timer = 0.0
        self.shot_count = 0
        self.last_heartbeat_time = 0.0

    def exit(self) -> None:
        """Called when exiting playing state."""
        pass

    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        process_gameplay_input(key, self.input_state)

        # Handle input actions
        if self.input_state.pause:
            self.game.state_manager.change_state("paused")
        elif self.input_state.quit:
            self.game.state_manager.change_state("menu")

    def update(self, dt: float) -> None:
        """Update gameplay logic.

        Args:
            dt: Delta time in seconds
        """
        self.frame_count += 1

        # Get settings
        player_mult, alien_mult, bullet_mult = self.settings.get_speed_multipliers()
        rapid_fire = self.settings.get("rapid_fire", False)
        bullet_hell = self.settings.get("bullet_hell", False)
        chaos_mode = self.settings.get("chaos_mode", False)

        # Apply chaos mode (random speed variations each frame)
        if chaos_mode:
            import random
            alien_mult *= random.uniform(0.5, 2.0)
            bullet_mult *= random.uniform(0.8, 1.5)

        # Apply speed multiplier to dt for aliens
        alien_dt = dt * alien_mult

        # Update player
        if self.input_state.move_left:
            self.player.move_left(dt)
        if self.input_state.move_right:
            self.player.move_right(dt)
        if self.input_state.shoot:
            # Rapid fire mode: bypass cooldown
            if rapid_fire:
                bullet = self.player.create_bullet()
                if bullet:
                    bullet.speed *= bullet_mult
                    self.bullets.append(bullet)
                    self.sound_manager.play_shoot()
                    self.shot_count += 1  # Track for mystery ship scoring
            else:
                bullet = self.player.shoot()
                if bullet:
                    bullet.speed *= bullet_mult
                    self.bullets.append(bullet)
                    self.sound_manager.play_shoot()
                    self.shot_count += 1  # Track for mystery ship scoring

        self.player.update(dt)

        # Update formation with modified dt
        self.formation.update(alien_dt)

        # Heartbeat sound disabled to prevent audio crashes
        # (was causing simpleaudio to crash with too many concurrent sounds)

        # Alien shooting (bullet hell: shoot more frequently)
        if bullet_hell and self.frame_count % 10 == 0:  # Extra shots
            alien_bullet = self.formation.try_shoot()
            if alien_bullet:
                alien_bullet.speed *= bullet_mult
                self.bullets.append(alien_bullet)

        alien_bullet = self.formation.try_shoot()
        if alien_bullet:
            alien_bullet.speed *= bullet_mult
            self.bullets.append(alien_bullet)

        # Mystery ship spawning and update
        self.mystery_ship_timer += dt
        if self.mystery_ship_timer >= self.mystery_ship_interval and not self.mystery_ship:
            # Spawn mystery ship
            import random
            direction = random.choice([-1, 1])
            self.mystery_ship = MysteryShip(direction)
            self.mystery_ship_timer = 0.0

        if self.mystery_ship:
            self.mystery_ship.update(dt)
            if not self.mystery_ship.alive:
                self.mystery_ship = None

        # Update bullets
        for bullet in self.bullets:
            bullet.update(dt)

        # Update effects
        self.effects.update(dt)

        # Update color effects
        self.color_effects.update()

        # Collision detection
        self._handle_collisions()

        # Remove dead bullets
        self.bullets = [b for b in self.bullets if b.alive]

        # Check win/lose conditions
        self._check_game_conditions()

    def _handle_collisions(self) -> None:
        """Handle all collision detection and resolution."""
        alive_aliens = self.formation.get_alive_aliens()

        # Bullets vs Aliens
        for bullet, alien in check_bullet_alien_collisions(self.bullets, alive_aliens):
            bullet.alive = False
            alien.alive = False
            self.game.score += alien.get_score_value()
            self.effects.add_explosion(int(alien.x), alien.y)
            self.sound_manager.play_explosion()

        # Bullets vs Mystery Ship
        if self.mystery_ship and self.mystery_ship.alive:
            for bullet in self.bullets:
                if bullet.alive and bullet.is_player:
                    from ..systems.collision import check_aabb_collision
                    if check_aabb_collision(bullet.get_bounds(), self.mystery_ship.get_bounds()):
                        bullet.alive = False
                        self.mystery_ship.alive = False

                        # Calculate mystery ship score based on shot count
                        mystery_score = self._calculate_mystery_ship_score()
                        self.mystery_ship.set_score_value(mystery_score)
                        self.game.score += mystery_score

                        mx, my = self.mystery_ship.get_position()
                        self.effects.add_explosion(mx, my)
                        self.sound_manager.play_explosion()
                        break

        # Bullets vs Shields
        for bullet, shield in check_bullet_shield_collisions(self.bullets, self.shields):
            bullet.alive = False
            shield.take_damage()

        # Alien bullets vs Player
        hit_bullet = check_bullet_player_collision(self.bullets, self.player)
        if hit_bullet:
            hit_bullet.alive = False
            self._player_hit()

        # Aliens vs Player (collision)
        if check_alien_player_collision(alive_aliens, self.player):
            self._player_hit()

        # Aliens reached bottom
        if check_aliens_reached_bottom(alive_aliens, PLAY_AREA_BOTTOM):
            self._player_hit()

    def _calculate_mystery_ship_score(self) -> int:
        """Calculate mystery ship score based on shot count.

        Classic Space Invaders scoring:
        - 23rd shot: 300 points
        - Every 15th shot after that: 300 points
        - Pattern: 23, 38, 53, 68, 83...
        - Otherwise: 50, 100, or 150 points

        Returns:
            Score value
        """
        # Check if this is the 23rd shot or every 15th after that
        if self.shot_count == 23:
            return 300
        elif self.shot_count > 23 and (self.shot_count - 23) % 15 == 0:
            return 300
        else:
            # Random other scores
            import random
            return random.choice([50, 100, 150])

    def _player_hit(self) -> None:
        """Handle player being hit."""
        invincible = self.settings.get("invincible", False)

        self.effects.add_explosion(int(self.player.x), self.player.y)
        self.sound_manager.play_explosion()

        if invincible:
            # In invincible mode, just show explosion but don't lose life
            return

        self.game.lives -= 1

        if self.game.lives <= 0:
            self.player.alive = False
            self.game.state_manager.change_state("game_over")
        else:
            # Reset player position
            self.player.reset()
            # Clear bullets
            self.bullets.clear()

    def _check_game_conditions(self) -> None:
        """Check for win/lose conditions."""
        # Check if level cleared
        if self.formation.is_cleared():
            self.sound_manager.play_level_complete()
            self.game.level += 1
            self.formation.reset(self.game.level)
            self.shields = create_shields()
            self.bullets.clear()

    def render(self, term: Terminal) -> None:
        """Render the gameplay.

        Args:
            term: Terminal instance
        """
        # Render UI
        render_ui(term, self.game.score, self.game.lives, self.game.level, self.game.high_score)

        # Render shields
        for i, shield in enumerate(self.shields):
            if shield.alive:
                sprite = shield.get_sprite()
                color = self.color_effects.get_color(shield.color, i + 100)
                for j, line in enumerate(sprite):
                    term.write_at(shield.x, shield.y + j, line, color)

        # Render aliens
        for i, alien in enumerate(self.formation.get_alive_aliens()):
            color = self.color_effects.get_alien_color(alien.color, i)
            for j, line in enumerate(alien.sprite):
                term.write_at(int(alien.x), alien.y + j, line, color)

        # Render mystery ship
        if self.mystery_ship and self.mystery_ship.alive:
            mx, my = self.mystery_ship.get_position()
            color = self.color_effects.get_color(self.mystery_ship.color, 500)
            for i, line in enumerate(self.mystery_ship.sprite):
                term.write_at(mx, my + i, line, color)

        # Render player
        if self.player.alive:
            color = self.color_effects.get_player_color(self.player.color)
            for i, line in enumerate(self.player.sprite):
                term.write_at(int(self.player.x), self.player.y + i, line, color)

        # Render bullets
        for bullet in self.bullets:
            if bullet.alive:
                x, y = bullet.get_position()
                is_player_bullet = bullet.char == "|"
                color = self.color_effects.get_bullet_color(bullet.color, is_player_bullet)
                term.write_at(x, y, bullet.char, color)

        # Render effects
        for explosion in self.effects.explosions:
            sprite = explosion.get_sprite()
            color = self.color_effects.get_color(explosion.color, self.frame_count)
            for i, line in enumerate(sprite):
                term.write_at(explosion.x, explosion.y + i, line, color)
