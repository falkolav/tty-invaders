"""Base state class for state machine."""
from abc import ABC, abstractmethod
from typing import Any, Optional

from ..renderer.terminal import Terminal


class BaseState(ABC):
    """Abstract base class for game states."""

    def __init__(self, game: Any) -> None:
        """Initialize the state.

        Args:
            game: Reference to the main game instance
        """
        self.game = game

    @abstractmethod
    def enter(self) -> None:
        """Called when entering this state."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Called when exiting this state."""
        pass

    @abstractmethod
    def handle_input(self, key: Any) -> None:
        """Handle keyboard input.

        Args:
            key: Key object from blessed
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update state logic.

        Args:
            dt: Delta time in seconds
        """
        pass

    @abstractmethod
    def render(self, term: Terminal) -> None:
        """Render the state.

        Args:
            term: Terminal instance
        """
        pass


class StateManager:
    """Manages game state transitions."""

    def __init__(self, game: Any) -> None:
        """Initialize the state manager.

        Args:
            game: Reference to the main game instance
        """
        self.game = game
        self.current_state: Optional[BaseState] = None
        self.states: dict[str, BaseState] = {}

    def add_state(self, name: str, state: BaseState) -> None:
        """Add a state to the manager.

        Args:
            name: State name identifier
            state: State instance
        """
        self.states[name] = state

    def change_state(self, name: str) -> None:
        """Change to a different state.

        Args:
            name: Name of the state to change to
        """
        if name not in self.states:
            raise ValueError(f"Unknown state: {name}")

        if self.current_state:
            self.current_state.exit()

        self.current_state = self.states[name]
        self.current_state.enter()

    def handle_input(self, key: Any) -> None:
        """Delegate input handling to current state.

        Args:
            key: Key object from blessed
        """
        if self.current_state:
            self.current_state.handle_input(key)

    def update(self, dt: float) -> None:
        """Delegate update to current state.

        Args:
            dt: Delta time in seconds
        """
        if self.current_state:
            self.current_state.update(dt)

    def render(self, term: Terminal) -> None:
        """Delegate rendering to current state.

        Args:
            term: Terminal instance
        """
        if self.current_state:
            self.current_state.render(term)
