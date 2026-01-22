"""ASCII sprites for game entities."""
from typing import List

# Player sprite
PLAYER_SPRITE = [
    " ▲ ",
    "███",
]

# Alien sprites (different types)
ALIEN_SPRITE_TOP = [
    " ▄▀▄ ",
    "█▀█▀█",
]

ALIEN_SPRITE_MID = [
    " ◢█◣ ",
    "▀███▀",
]

ALIEN_SPRITE_BOT = [
    " ╱█╲ ",
    "◢███◣",
]

# Alternative alien animation frames
ALIEN_SPRITE_TOP_ALT = [
    " ▀▄▀ ",
    "█▄█▄█",
]

ALIEN_SPRITE_MID_ALT = [
    " ◥█◤ ",
    "▄███▄",
]

ALIEN_SPRITE_BOT_ALT = [
    " ╲█╱ ",
    "◥███◤",
]

# Shield sprite
SHIELD_SPRITE = [
    "████████",
    "███  ███",
    "██    ██",
]

# Shield damaged states
SHIELD_SPRITE_DAMAGED_1 = [
    "█ ██ ███",
    "███  █ █",
    "██   ██",
]

SHIELD_SPRITE_DAMAGED_2 = [
    "█ ██  ██",
    "█ █  █ █",
    "█    ██",
]

SHIELD_SPRITE_DAMAGED_3 = [
    "█  █  ██",
    "█ █   █ ",
    "█    █ ",
]

# Explosion animation frames
EXPLOSION_FRAMES = [
    [" * "],
    [" ╳ "],
    ["*╳*"],
    ["╳*╳"],
    [" * "],
    ["   "],
]

# Simple bullet sprites (single char)
BULLET_PLAYER = "|"
BULLET_ALIEN = "!"


def get_alien_sprite(row: int, animated: bool = False) -> List[str]:
    """Get alien sprite based on row position.

    Args:
        row: Row number (0-indexed from top)
        animated: Whether to use alternate animation frame

    Returns:
        List of sprite lines
    """
    if row == 0:
        return ALIEN_SPRITE_TOP_ALT if animated else ALIEN_SPRITE_TOP
    elif row <= 2:
        return ALIEN_SPRITE_MID_ALT if animated else ALIEN_SPRITE_MID
    else:
        return ALIEN_SPRITE_BOT_ALT if animated else ALIEN_SPRITE_BOT


def get_shield_sprite(health_percent: float) -> List[str]:
    """Get shield sprite based on health percentage.

    Args:
        health_percent: Health as percentage (0.0 - 1.0)

    Returns:
        List of sprite lines
    """
    if health_percent > 0.75:
        return SHIELD_SPRITE
    elif health_percent > 0.5:
        return SHIELD_SPRITE_DAMAGED_1
    elif health_percent > 0.25:
        return SHIELD_SPRITE_DAMAGED_2
    else:
        return SHIELD_SPRITE_DAMAGED_3


def get_sprite_width(sprite: List[str]) -> int:
    """Get the width of a sprite.

    Args:
        sprite: List of sprite lines

    Returns:
        Maximum width of sprite lines
    """
    return max(len(line) for line in sprite) if sprite else 0


def get_sprite_height(sprite: List[str]) -> int:
    """Get the height of a sprite.

    Args:
        sprite: List of sprite lines

    Returns:
        Number of lines in sprite
    """
    return len(sprite)
