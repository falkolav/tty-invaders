"""Options/Settings state."""
from typing import Any, List, Tuple

from .base import BaseState
from ..renderer.terminal import Terminal
from ..config import GAME_WIDTH


class OptionsState(BaseState):
    """Options menu state for game customization."""

    def __init__(self, game: Any) -> None:
        """Initialize options state.

        Args:
            game: Reference to the main game instance
        """
        super().__init__(game)
        self.menu_items: List[Tuple[str, str, List[Any]]] = []
        self.selected_index = 0
        self.settings = None

    def enter(self) -> None:
        """Called when entering options state."""
        from ..utils.settings import GameSettings

        self.settings = GameSettings()
        self.selected_index = 0
        self._build_menu()

    def exit(self) -> None:
        """Called when exiting options state."""
        if self.settings:
            self.settings.save()

    def _build_menu(self) -> None:
        """Build the menu items dynamically."""
        self.menu_items = [
            ("GAME MODE", "game_mode", [
                ("Normal", "normal"),
                ("Slow-Mo (Bullet Time)", "slow_mo"),
                ("Turbo (Speed Demon)", "turbo"),
                ("Insane (Total Chaos)", "insane"),
                ("Zen (Chill Mode)", "zen"),
                ("Nightmare (Ultra Hard)", "nightmare"),
                ("SUPERDUPERCRAZY", "superdupercrazy")
            ]),
            ("SOUND", "sound_enabled", [
                ("On", True),
                ("Off", False)
            ]),
            ("", "back", [("< Back to Menu", "back")])
        ]

    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        if not key:
            return

        key_name = key.name if hasattr(key, 'name') else str(key)

        if key_name == "KEY_UP" or key == "w" or key == "W":
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif key_name == "KEY_DOWN" or key == "s" or key == "S":
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif key_name == "KEY_LEFT" or key == "a" or key == "A":
            self._change_option(-1)
        elif key_name == "KEY_RIGHT" or key == "d" or key == "D":
            self._change_option(1)
        elif key_name == "KEY_ENTER" or key == " ":
            self._select_option()
        elif key_name == "KEY_ESCAPE" or key == "q" or key == "Q":
            self.settings.save()
            self.game.state_manager.change_state("menu")

    def _change_option(self, direction: int) -> None:
        """Change the selected option value.

        Args:
            direction: -1 for left, 1 for right
        """
        if self.selected_index >= len(self.menu_items):
            return

        name, key, options = self.menu_items[self.selected_index]

        if key == "back":
            return

        # Get current value
        current_value = self.settings.get(key)

        # Find current index in options
        current_index = 0
        for i, (_, value) in enumerate(options):
            if value == current_value:
                current_index = i
                break

        # Change to next/prev option
        new_index = (current_index + direction) % len(options)
        _, new_value = options[new_index]

        # Apply the setting
        if key == "game_mode":
            self.settings.apply_game_mode(new_value)
            self._build_menu()  # Rebuild menu to reflect preset changes
        else:
            self.settings.set(key, new_value)

            # Update sound manager if sound setting changed
            if key == "sound_enabled":
                self.game.sound_manager.enabled = new_value

    def _select_option(self) -> None:
        """Handle selection of current option."""
        if self.selected_index >= len(self.menu_items):
            return

        name, key, options = self.menu_items[self.selected_index]

        if key == "back":
            self.settings.save()
            self.game.state_manager.change_state("menu")
        else:
            # Cycle to next option
            self._change_option(1)

    def update(self, dt: float) -> None:
        """Update options logic.

        Args:
            dt: Delta time in seconds
        """
        pass

    def render(self, term: Terminal) -> None:
        """Render the options menu.

        Args:
            term: Terminal instance
        """
        # Title
        title = "⚙ OPTIONS ⚙"
        term.write_at((GAME_WIDTH - len(title)) // 2, 2, title, "cyan")

        subtitle = "Customize Your Experience"
        term.write_at((GAME_WIDTH - len(subtitle)) // 2, 3, subtitle, "bright_black")

        # Menu items
        y = 6
        for i, (name, key, options) in enumerate(self.menu_items):
            if key == "back":
                # Back button
                y += 1
                text = "< Back to Menu"
                color = "yellow" if i == self.selected_index else "white"
                term.write_at((GAME_WIDTH - len(text)) // 2, y, text, color)
            else:
                # Get current value
                current_value = self.settings.get(key)
                current_label = ""
                for label, value in options:
                    if value == current_value:
                        current_label = label
                        break

                # Render option name
                color = "yellow" if i == self.selected_index else "white"
                indicator = "►" if i == self.selected_index else " "

                option_text = f"{indicator} {name}"
                term.write_at(10, y, option_text, color)

                # Render current value with arrows
                value_text = f"< {current_label} >"
                value_x = GAME_WIDTH - len(value_text) - 10
                term.write_at(value_x, y, value_text, color)

                y += 2

        # Help text
        help_y = term.height - 4
        help_texts = [
            "↑↓ / WS: Navigate  |  ←→ / AD: Change  |  ENTER: Select  |  ESC / Q: Back"
        ]
        for i, help_text in enumerate(help_texts):
            term.write_at((GAME_WIDTH - len(help_text)) // 2, help_y + i, help_text, "bright_black")

        # Mode descriptions
        desc_y = help_y - 3
        descriptions = {
            "normal": "Classic Space Invaders experience",
            "slow_mo": "Time slows down, Matrix-style combat",
            "turbo": "Everything is super fast and intense",
            "insane": "CHAOS! Random speeds, rapid fire, maximum mayhem",
            "zen": "Relaxing mode - you can't die",
            "nightmare": "Prepare to suffer. Good luck.",
            "superdupercrazy": "ABSOLUTELY BONKERS! Maximum speed, chaos, mayhem!",
        }

        current_mode = self.settings.get("game_mode")
        if current_mode in descriptions:
            desc = descriptions[current_mode]
            term.write_at((GAME_WIDTH - len(desc)) // 2, desc_y, desc, "bright_black")
