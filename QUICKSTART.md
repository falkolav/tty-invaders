# TTY Invaders - Quick Start Guide

## Installation & Running

```bash
# 1. Install dependencies
uv sync

# 2. Run the game (choose one):

# Method 1: Using script name (note: hyphen, not underscore!)
uv run tty-invaders

# Method 2: Running as Python module
uv run python -m tty_invaders

# Method 3: Direct execution
.venv/bin/tty-invaders
```

**Important:** The script name uses a hyphen (`tty-invaders`) while the Python package uses an underscore (`tty_invaders`).

## Controls

### Menu
- `↑/↓` or `W/S` - Navigate
- `Enter/Space` - Select
- `Q/ESC` - Quit

### Gameplay
- `←/→` or `A/D` - Move
- `Space/Enter` - Shoot
- `P/ESC` - Pause
- `Q` - Return to menu

## Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_collision.py -v
```

## Development

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy tty_invaders
```

## Game Features Implemented

✅ **Phase 1 - Foundation**
- Project structure with uv package manager
- Terminal wrapper with blessed
- Main game loop with 60 FPS fixed timestep
- State machine (BaseState, StateManager)
- Menu state with navigation

✅ **Phase 2 - Core Gameplay**
- Player entity with movement and shooting
- Alien entity with different types
- Bullet entity (player and alien bullets)
- ASCII/Unicode sprites for all entities
- Movement system with delta time
- Input handling system
- UI rendering (score, lives, level)

✅ **Phase 3 - Game Mechanics**
- AABB collision detection
- Alien formation manager with AI
- Alien shooting behavior
- Destructible shields with degradation
- Scoring system
- Win/lose conditions
- Complete PlayingState

✅ **Phase 4 - Polish & Features**
- Explosion animations
- Sound system (with beepy)
- Progressive difficulty (speed, frequency, formation size)
- Level progression
- High score persistence (JSON)
- GameOverState with name entry
- LeaderboardState with top 10
- PausedState

✅ **Phase 5 - Testing & Documentation**
- 38 unit tests (all passing)
  - Collision detection tests
  - Entity behavior tests
  - Scoring system tests
  - Persistence tests
- Comprehensive README
- Quick start guide
- Project well-documented with docstrings

## Architecture Highlights

- **Component-based entities**: Player, Alien, Bullet, Shield
- **State machine**: Menu, Playing, Paused, GameOver, Leaderboard
- **Fixed timestep**: 60 FPS with delta time movement
- **AABB collision**: Efficient bounding box detection
- **JSON persistence**: High scores saved locally

## File Count

- **30 Python files** (including tests)
- **38 unit tests** (100% passing)
- Clean architecture with separation of concerns

## Next Steps

1. Run the game: `uv run tty-invaders`
2. Play through a few levels
3. Try to get a high score!
4. Check the leaderboard

Enjoy! 🚀👾
