"""Game configuration and constants."""

# Display settings
MIN_TERMINAL_WIDTH = 80
MIN_TERMINAL_HEIGHT = 24
FPS = 60
FRAME_TIME = 1.0 / FPS

# Game area
GAME_WIDTH = 80
GAME_HEIGHT = 24
PLAY_AREA_TOP = 3  # Reserve top rows for UI
PLAY_AREA_BOTTOM = GAME_HEIGHT - 1

# Player settings
PLAYER_START_Y = PLAY_AREA_BOTTOM - 2
PLAYER_START_X = GAME_WIDTH // 2
PLAYER_SPEED = 90  # Characters per second (50% increase for highly responsive controls)
PLAYER_LIVES = 3
PLAYER_SHOOT_COOLDOWN = 0.3  # Seconds between shots

# Bullet settings
BULLET_SPEED = 40  # Characters per second
PLAYER_BULLET_CHAR = "|"
ALIEN_BULLET_CHAR = "!"

# Alien settings
ALIEN_COLS = 11
ALIEN_ROWS = 5
ALIEN_SPACING_X = 5
ALIEN_SPACING_Y = 2
ALIEN_START_X = 5
ALIEN_START_Y = PLAY_AREA_TOP + 2
ALIEN_BASE_SPEED = 5  # Characters per second (reduced for easier first level)
ALIEN_SPEED_INCREMENT = 1.5  # Speed increase per level
ALIEN_DESCENT = 1  # Rows to move down when hitting edge
ALIEN_BASE_SHOOT_FREQ = 2.5  # Seconds between shots (increased for easier start)
ALIEN_SHOOT_FREQ_DECREMENT = 0.15  # Decrease per level

# Scoring (Classic Space Invaders)
SCORE_ALIEN_TOP = 30  # Top row aliens (small/squid)
SCORE_ALIEN_MID = 20  # Middle rows aliens (medium/crab)
SCORE_ALIEN_BOT = 10  # Bottom rows aliens (large/octopus)

# Shield settings
SHIELD_COUNT = 4
SHIELD_Y = PLAYER_START_Y - 5
SHIELD_WIDTH = 8
SHIELD_HEIGHT = 3
SHIELD_HEALTH = 10  # Hits before destruction

# Difficulty progression
MAX_ALIEN_ROWS = 7
MIN_SHOOT_FREQUENCY = 0.5

# High scores
MAX_HIGH_SCORES = 10
HIGH_SCORE_FILE = "scores.json"

# Colors (blessed color names)
COLOR_PLAYER = "green"
COLOR_ALIEN_TOP = "red"
COLOR_ALIEN_MID = "yellow"
COLOR_ALIEN_BOT = "cyan"
COLOR_BULLET_PLAYER = "white"
COLOR_BULLET_ALIEN = "red"
COLOR_SHIELD = "blue"
COLOR_UI = "white"
COLOR_MENU = "cyan"
COLOR_EXPLOSION = "yellow"

# Sound
SOUND_ENABLED = True
SOUND_SHOOT = 1  # beepy sound ID
SOUND_EXPLOSION = 2
SOUND_GAME_OVER = 3
