# TTY Invaders

A polished terminal-based Space Invaders game in Python with classic gameplay, progressive difficulty, high scores, and sound effects.

## Features

- 🎮 Classic Space Invaders gameplay
- 🚀 Smooth 60 FPS game loop
- 👾 Progressive difficulty across levels
- 🛡️ Destructible shields
- 🏆 Persistent high score leaderboard
- 🎵 Sound effects (optional)
- ⌨️ Intuitive keyboard controls
- 🎨 Colorful ASCII graphics

## Requirements

- Python 3.11 or higher
- Terminal with minimum 80x24 characters
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

### Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### Install the game

```bash
# Clone the repository
cd tty-invaders

# Install dependencies
uv sync

# Run the game (choose one method):
# Method 1: Using the installed script (note: hyphen, not underscore)
uv run tty-invaders

# Method 2: Running as a Python module
uv run python -m tty_invaders

# Method 3: Direct execution from venv
.venv/bin/tty-invaders
```

## How to Play

### Controls

**Menu Navigation:**
- `↑` / `↓` or `W` / `S` - Navigate menu options
- `Enter` / `Space` - Select option
- `Q` / `ESC` - Quit

**Gameplay:**
- `←` / `→` or `A` / `D` - Move player left/right
- `Space` / `Enter` - Shoot
- `P` / `ESC` - Pause game
- `Q` - Return to menu

### Objective

- Destroy all aliens before they reach the bottom
- Use shields for protection
- Survive and advance through increasingly difficult levels
- Achieve the highest score!

### Scoring

- Bottom row aliens: 10 points
- Middle row aliens: 20 points
- Top row aliens: 30 points

## Gameplay Mechanics

### Progressive Difficulty

Each level increases the challenge:
- Aliens move faster
- Aliens shoot more frequently
- More rows of aliens appear (up to 7 rows)

### Shields

- 4 destructible shields protect the player
- Shields degrade with each hit
- Use them strategically!

### Lives

- Start with 3 lives
- Lose a life when hit by alien bullet or collision
- Game over when all lives are lost

## High Scores

High scores are automatically saved to `scores.json` in the project directory. Enter your 3-letter name when you achieve a top-10 score!

## Development

### Run Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy tty_invaders
```

## Project Structure

```
tty-invaders/
├── tty_invaders/          # Main package
│   ├── states/            # Game states (menu, playing, etc.)
│   ├── entities/          # Game objects (player, aliens, etc.)
│   ├── systems/           # Game logic (collision, input, etc.)
│   ├── renderer/          # Display and UI
│   ├── audio/             # Sound effects
│   └── utils/             # Utilities (timing, persistence)
├── tests/                 # Unit tests
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Technical Details

- **Architecture**: Component-based entity system with state machine
- **Game Loop**: Fixed timestep at 60 FPS with delta time
- **Collision**: AABB (Axis-Aligned Bounding Box) detection
- **Terminal Library**: Blessed (cross-platform)
- **Sound**: Beepy (optional, with graceful fallback)

## Troubleshooting

**Command not found: `tty_invaders`**
- Use `tty-invaders` (with hyphen, not underscore)
- Correct: `uv run tty-invaders`
- Alternative: `uv run python -m tty_invaders`

**Terminal too small error:**
- Resize your terminal to at least 80x24 characters
- Some terminals: `Cmd +` / `Ctrl +` to increase size

**Color/TypeError issues:**
- Make sure you have the latest version: `uv sync --reinstall`
- All color names have been fixed to use valid blessed colors

**No sound:**
- Sound effects are optional
- Game works fine without sound
- Check that `beepy` is installed: `uv sync`

**Game runs slowly:**
- Ensure your terminal supports 60 FPS rendering
- Try a different terminal emulator (iTerm2, Terminal.app, etc.)
- Check CPU usage

## Credits

Created as a modern take on the classic Space Invaders arcade game.

Built with:
- Python 3.11+
- Blessed (terminal control)
- Beepy (sound effects)
- uv (package management)

## License

This is a personal project for educational purposes.

---

**Have fun defending Earth! 🌍👾🚀**
