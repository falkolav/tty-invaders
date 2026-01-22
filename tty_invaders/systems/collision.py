"""Collision detection system."""
from typing import Any, Optional


def check_aabb_collision(box1: tuple[int, int, int, int],
                         box2: tuple[int, int, int, int]) -> bool:
    """Check Axis-Aligned Bounding Box collision.

    Args:
        box1: Tuple of (x, y, width, height)
        box2: Tuple of (x, y, width, height)

    Returns:
        True if boxes overlap
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)


def check_bullet_alien_collisions(bullets: list[Any], aliens: list[Any]) -> list[tuple[Any, Any]]:
    """Check collisions between bullets and aliens.

    Args:
        bullets: List of Bullet instances
        aliens: List of Alien instances

    Returns:
        List of (bullet, alien) collision pairs
    """
    collisions = []

    for bullet in bullets:
        if not bullet.alive or not bullet.is_player:
            continue

        bullet_bounds = bullet.get_bounds()

        for alien in aliens:
            if not alien.alive:
                continue

            alien_bounds = alien.get_bounds()

            if check_aabb_collision(bullet_bounds, alien_bounds):
                collisions.append((bullet, alien))
                break  # Bullet can only hit one alien

    return collisions


def check_bullet_shield_collisions(bullets: list[Any], shields: list[Any]) -> list[tuple[Any, Any]]:
    """Check collisions between bullets and shields.

    Args:
        bullets: List of Bullet instances
        shields: List of Shield instances

    Returns:
        List of (bullet, shield) collision pairs
    """
    collisions = []

    for bullet in bullets:
        if not bullet.alive:
            continue

        bullet_bounds = bullet.get_bounds()

        for shield in shields:
            if not shield.alive:
                continue

            shield_bounds = shield.get_bounds()

            if check_aabb_collision(bullet_bounds, shield_bounds):
                collisions.append((bullet, shield))
                break  # Bullet can only hit one shield

    return collisions


def check_bullet_player_collision(bullets: list[Any], player: Any) -> Optional[Any]:
    """Check collisions between alien bullets and player.

    Args:
        bullets: List of Bullet instances
        player: Player instance

    Returns:
        First bullet that hit player, or None
    """
    if not player.alive:
        return None

    player_bounds = player.get_bounds()

    for bullet in bullets:
        if not bullet.alive or bullet.is_player:
            continue

        bullet_bounds = bullet.get_bounds()

        if check_aabb_collision(bullet_bounds, player_bounds):
            return bullet

    return None


def check_alien_player_collision(aliens: list[Any], player: Any) -> bool:
    """Check if any alien has collided with the player.

    Args:
        aliens: List of Alien instances
        player: Player instance

    Returns:
        True if collision detected
    """
    if not player.alive:
        return False

    player_bounds = player.get_bounds()

    for alien in aliens:
        if not alien.alive:
            continue

        alien_bounds = alien.get_bounds()

        if check_aabb_collision(alien_bounds, player_bounds):
            return True

    return False


def check_aliens_reached_bottom(aliens: list[Any], bottom_y: int) -> bool:
    """Check if any alien has reached the bottom of the play area.

    Args:
        aliens: List of Alien instances
        bottom_y: Y coordinate of bottom boundary

    Returns:
        True if any alien reached bottom
    """
    for alien in aliens:
        if not alien.alive:
            continue

        if alien.y + alien.height >= bottom_y:
            return True

    return False
