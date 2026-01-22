"""Sound manager using pygame.mixer for retro sound effects."""
from pathlib import Path
from typing import Optional
from ..config import SOUND_ENABLED


class SoundManager:
    """Manages game sound effects using pygame.mixer.

    Falls back to terminal bell if pygame is unavailable or initialization fails.
    """

    def __init__(self, enabled: bool = SOUND_ENABLED) -> None:
        """Initialize sound manager.

        Args:
            enabled: Whether sound is enabled
        """
        self.enabled = enabled
        self.muted = False
        self.use_pygame = False
        self.sounds: dict[str, any] = {}

        # Try to initialize pygame.mixer
        self._init_pygame()

    def _init_pygame(self) -> None:
        """Initialize pygame mixer and load sound files."""
        try:
            import pygame

            # Initialize only the mixer (not full pygame display)
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.use_pygame = True

            # Load sound files if they exist
            sounds_dir = Path(__file__).parent / "sounds"
            if sounds_dir.exists():
                self._load_sounds(sounds_dir)
        except Exception:
            # Fall back to terminal bell if pygame fails
            self.use_pygame = False

    def _load_sounds(self, sounds_dir: Path) -> None:
        """Load sound files from directory.

        Args:
            sounds_dir: Directory containing sound files
        """
        try:
            import pygame

            sound_files = {
                "shoot": "shoot.wav",
                "explosion": "invaderkilled.wav",
                "game_over": "invaderkilled.wav",  # Reuse for now
                "level_complete": "ufo_highpitch.wav",  # Reuse for now
                "ufo": "ufo_lowpitch.wav",
                "heartbeat1": "fastinvader1.wav",
                "heartbeat2": "fastinvader2.wav",
                "heartbeat3": "fastinvader3.wav",
                "heartbeat4": "fastinvader4.wav",
            }

            for name, filename in sound_files.items():
                filepath = sounds_dir / filename
                if filepath.exists():
                    self.sounds[name] = pygame.mixer.Sound(str(filepath))
        except Exception:
            # If loading fails, sounds dict stays empty
            pass

    def _play_sound(self, sound_name: str) -> None:
        """Play a sound effect.

        Args:
            sound_name: Name of the sound to play
        """
        if not self._can_play():
            return

        if self.use_pygame and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception:
                # Fall back to terminal bell if playback fails
                self._terminal_bell()
        else:
            # Fall back to terminal bell
            self._terminal_bell()

    def play_shoot(self) -> None:
        """Play shooting sound effect."""
        self._play_sound("shoot")

    def play_explosion(self) -> None:
        """Play explosion sound effect."""
        self._play_sound("explosion")

    def play_game_over(self) -> None:
        """Play game over sound effect."""
        self._play_sound("game_over")

    def play_level_complete(self) -> None:
        """Play level complete sound effect."""
        self._play_sound("level_complete")

    def play_heartbeat(self, speed_level: int = 0) -> None:
        """Heartbeat disabled for now."""
        pass

    def play_ufo(self) -> None:
        """UFO sound disabled for now."""
        pass

    def stop_ufo(self) -> None:
        """UFO sound disabled for now."""
        pass

    def _terminal_bell(self) -> None:
        """Play terminal bell sound as fallback."""
        try:
            print('\a', end='', flush=True)
        except:
            pass

    def toggle_mute(self) -> None:
        """Toggle mute on/off."""
        self.muted = not self.muted

    def _can_play(self) -> bool:
        """Check if sound can be played.

        Returns:
            True if sound is enabled and not muted
        """
        return self.enabled and not self.muted
