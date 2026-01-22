"""Game settings manager."""
import json
from pathlib import Path
from typing import Any, Dict


class GameSettings:
    """Manages game settings and options."""

    DEFAULT_SETTINGS = {
        # Audio
        "sound_enabled": True,

        # Speed modifiers (multipliers)
        "player_speed_multiplier": 1.0,
        "alien_speed_multiplier": 1.0,
        "bullet_speed_multiplier": 1.0,

        # Visual options
        "color_mode": "normal",  # normal, rainbow, disco, matrix, psychedelic
        "show_trails": False,

        # Gameplay modifiers
        "rapid_fire": False,  # No shoot cooldown
        "bullet_hell": False,  # Aliens shoot way more
        "invincible": False,  # Player can't die
        "chaos_mode": False,  # Random speeds and behaviors

        # Extreme presets
        "game_mode": "normal",  # normal, slow_mo, turbo, insane, zen, nightmare, superdupercrazy
    }

    def __init__(self, settings_file: str = "settings.json") -> None:
        """Initialize settings manager.

        Args:
            settings_file: Path to settings file
        """
        self.settings_file = Path(settings_file)
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self.load()

    def load(self) -> None:
        """Load settings from file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Update with loaded settings, keeping defaults for missing keys
                    self.settings.update(loaded)
            except Exception:
                # If loading fails, use defaults
                pass

    def save(self) -> None:
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_SETTINGS.copy()

    def apply_game_mode(self, mode: str) -> None:
        """Apply a game mode preset.

        Args:
            mode: Game mode name
        """
        self.set("game_mode", mode)

        if mode == "normal":
            self.set("player_speed_multiplier", 1.0)
            self.set("alien_speed_multiplier", 1.0)
            self.set("bullet_speed_multiplier", 1.0)
            self.set("rapid_fire", False)
            self.set("bullet_hell", False)
            self.set("chaos_mode", False)
            self.set("color_mode", "normal")
            self.set("invincible", False)

        elif mode == "slow_mo":
            # Bullet time mode
            self.set("player_speed_multiplier", 1.5)
            self.set("alien_speed_multiplier", 0.3)
            self.set("bullet_speed_multiplier", 0.5)
            self.set("color_mode", "matrix")

        elif mode == "turbo":
            # Everything is fast
            self.set("player_speed_multiplier", 2.0)
            self.set("alien_speed_multiplier", 1.8)
            self.set("bullet_speed_multiplier", 2.0)
            self.set("rapid_fire", True)
            self.set("color_mode", "rainbow")

        elif mode == "insane":
            # Absolute chaos
            self.set("player_speed_multiplier", 3.0)
            self.set("alien_speed_multiplier", 2.5)
            self.set("bullet_speed_multiplier", 2.5)
            self.set("rapid_fire", True)
            self.set("bullet_hell", True)
            self.set("chaos_mode", True)
            self.set("color_mode", "psychedelic")

        elif mode == "zen":
            # Chill mode
            self.set("player_speed_multiplier", 0.7)
            self.set("alien_speed_multiplier", 0.5)
            self.set("bullet_speed_multiplier", 0.8)
            self.set("invincible", True)
            self.set("color_mode", "matrix")

        elif mode == "nightmare":
            # Ultra hard
            self.set("player_speed_multiplier", 0.8)
            self.set("alien_speed_multiplier", 2.0)
            self.set("bullet_speed_multiplier", 1.5)
            self.set("bullet_hell", True)
            self.set("rapid_fire", False)
            self.set("color_mode", "disco")

        elif mode == "superdupercrazy":
            # ABSOLUTELY BONKERS - everything is maxed out and chaotic
            self.set("player_speed_multiplier", 5.0)
            self.set("alien_speed_multiplier", 4.0)
            self.set("bullet_speed_multiplier", 4.5)
            self.set("rapid_fire", True)
            self.set("bullet_hell", True)
            self.set("chaos_mode", True)
            self.set("color_mode", "psychedelic")
            self.set("show_trails", True)

    def get_speed_multipliers(self) -> tuple[float, float, float]:
        """Get all speed multipliers.

        Returns:
            Tuple of (player, alien, bullet) speed multipliers
        """
        return (
            self.get("player_speed_multiplier", 1.0),
            self.get("alien_speed_multiplier", 1.0),
            self.get("bullet_speed_multiplier", 1.0)
        )
