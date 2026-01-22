# Changelog

All notable changes to TTY Invaders will be documented in this file.

## [1.0.2] - 2026-01-22

### Changed
- **Reduced alien speed in level 1** from 10 to 5 chars/sec (50% slower) for better difficulty balance
- **Aliens shoot less frequently** at start: 2.5 seconds between shots (was 2.0 seconds)
- **Gentler difficulty curve**: Speed increment reduced from 2.0 to 1.5 per level
- Level 1 is now much more beginner-friendly while still maintaining challenge in later levels

### Difficulty Progression
- Level 1: 5.0 chars/sec (was 10.0)
- Level 2: 6.5 chars/sec (was 12.0)
- Level 3: 8.0 chars/sec (was 14.0)
- Level 4: 9.5 chars/sec (was 16.0)
- Level 5: 11.0 chars/sec (was 18.0)

## [1.0.1] - 2026-01-22

### Changed
- **Doubled player movement speed** from 30 to 60 characters per second for more responsive controls
- **High score now displays in bright yellow** instead of white to make it more prominent during gameplay
- **Score and lives display in bright white** for better visibility

### Added
- **Dynamic terminal resize handling** - Game now automatically adjusts when you resize the terminal window
- Terminal size is checked each frame and screen is redrawn cleanly on resize

### Fixed
- Fixed `dark_gray` color errors by replacing with valid `bright_black` color
- Fixed command naming confusion (script is `tty-invaders` with hyphen, not underscore)

## [1.0.0] - 2026-01-22

### Initial Release
- Complete Space Invaders implementation in terminal
- 60 FPS game loop with delta time
- Progressive difficulty across levels
- Destructible shields
- High score persistence with leaderboard
- Sound effects (optional)
- 5 game states: Menu, Playing, Paused, GameOver, Leaderboard
- 38 unit tests (100% passing)
- Full documentation

### Features
- Player movement and shooting
- Alien formation AI with animation
- AABB collision detection
- Explosion effects
- Multiple alien types with different scores
- Level progression with increasing difficulty
