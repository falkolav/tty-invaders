"""UI rendering for score, lives, and level display."""
from .terminal import Terminal
from ..config import COLOR_UI, GAME_WIDTH


def render_ui(term: Terminal, score: int, lives: int, level: int, high_score: int) -> None:
    """Render the game UI (score, lives, level).

    Args:
        term: Terminal instance
        score: Current score
        lives: Remaining lives
        level: Current level
        high_score: High score
    """
    # Top bar
    term.write_at(0, 0, "=" * GAME_WIDTH, COLOR_UI)

    # Score (left side)
    score_text = f"SCORE: {score:06d}"
    term.write_at(2, 1, score_text, "bright_white")

    # High score (center) - make it stand out with bright yellow
    high_score_text = f"HI-SCORE: {high_score:06d}"
    x = (GAME_WIDTH - len(high_score_text)) // 2
    term.write_at(x, 1, high_score_text, "bright_yellow")

    # Lives and level (right side)
    lives_text = f"LIVES: {lives}"
    level_text = f"LVL: {level}"
    info_text = f"{lives_text}  {level_text}"
    x = GAME_WIDTH - len(info_text) - 2
    term.write_at(x, 1, info_text, "bright_white")

    # Bottom bar
    term.write_at(0, 2, "=" * GAME_WIDTH, COLOR_UI)


def render_menu(term: Terminal, title: str, options: list[tuple[str, bool]],
                footer: str = "") -> None:
    """Render a menu screen.

    Args:
        term: Terminal instance
        title: Menu title
        options: List of (option_text, is_selected) tuples
        footer: Optional footer text
    """
    height = term.height
    width = GAME_WIDTH

    # Clear and draw border
    term.clear()
    term.write_at(0, 0, "╔" + "═" * (width - 2) + "╗", COLOR_UI)
    for y in range(1, height - 1):
        term.write_at(0, y, "║", COLOR_UI)
        term.write_at(width - 1, y, "║", COLOR_UI)
    term.write_at(0, height - 1, "╚" + "═" * (width - 2) + "╝", COLOR_UI)

    # Title
    title_y = height // 4
    title_x = (width - len(title)) // 2
    term.write_at(title_x, title_y, title, "bright_cyan")

    # Options
    start_y = height // 2 - len(options)
    for i, (option, selected) in enumerate(options):
        y = start_y + i * 2
        prefix = "► " if selected else "  "
        option_text = prefix + option
        x = (width - len(option_text)) // 2
        color = "bright_white" if selected else "white"
        term.write_at(x, y, option_text, color)

    # Footer
    if footer:
        footer_y = height - 3
        footer_x = (width - len(footer)) // 2
        term.write_at(footer_x, footer_y, footer, "bright_black")


def render_game_over(term: Terminal, score: int, is_high_score: bool) -> None:
    """Render game over screen.

    Args:
        term: Terminal instance
        score: Final score
        is_high_score: Whether this is a new high score
    """
    height = term.height
    width = GAME_WIDTH

    game_over_text = "GAME OVER"
    score_text = f"FINAL SCORE: {score:06d}"

    y = height // 2 - 2
    term.write_at((width - len(game_over_text)) // 2, y, game_over_text, "red")

    y += 2
    term.write_at((width - len(score_text)) // 2, y, score_text, COLOR_UI)

    if is_high_score:
        y += 2
        high_score_msg = "NEW HIGH SCORE!"
        term.write_at((width - len(high_score_msg)) // 2, y, high_score_msg, "yellow")


def render_level_complete(term: Terminal, level: int) -> None:
    """Render level complete screen.

    Args:
        term: Terminal instance
        level: Completed level number
    """
    height = term.height
    width = GAME_WIDTH

    text = f"LEVEL {level} COMPLETE!"
    next_text = "Get ready..."

    y = height // 2
    term.write_at((width - len(text)) // 2, y, text, "green")
    term.write_at((width - len(next_text)) // 2, y + 2, next_text, COLOR_UI)


def render_paused(term: Terminal) -> None:
    """Render paused overlay.

    Args:
        term: Terminal instance
    """
    height = term.height
    width = GAME_WIDTH

    text = "PAUSED"
    resume_text = "Press P to resume"

    y = height // 2
    term.write_at((width - len(text)) // 2, y, text, "yellow")
    term.write_at((width - len(resume_text)) // 2, y + 2, resume_text, COLOR_UI)
