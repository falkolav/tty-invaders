# TTY Invaders - Recent Improvements (v1.0.1)

## Player Experience Improvements

### 1. ⚡ Faster Player Movement
**Before:** Player moved at 30 characters/second
**After:** Player moves at 60 characters/second (2x faster)
**Impact:** Much more responsive controls, easier to dodge alien bullets

### 2. 📐 Dynamic Window Resize
**Before:** Game didn't adapt to terminal size changes
**After:** Game automatically detects and adapts to window resizing
**Impact:** You can now resize your terminal window while playing and the game will adjust

### 3. 👁️ Better High Score Visibility
**Before:** High score displayed in plain white
**After:** High score in bright yellow, current score in bright white
**Impact:** High score stands out prominently at the top center of the screen

## Visual Comparison

### UI Display (Top Bar)
```
Before:
====================================================================
SCORE: 000150        HI-SCORE: 001000        LIVES: 3  LVL: 1
====================================================================

After:
====================================================================
SCORE: 000150        HI-SCORE: 001000        LIVES: 3  LVL: 1
====================================================================
(with HI-SCORE in bright yellow, SCORE and LIVES in bright white)
```

### Movement Speed Comparison
```
Before: ▲ → → →      (moves 3 spaces in 0.1 seconds)
After:  ▲ → → → → →  (moves 6 spaces in 0.1 seconds)
```

## Technical Details

### Movement Speed
- **File changed:** `tty_invaders/config.py`
- **Line:** `PLAYER_SPEED = 60` (was 30)
- **Formula:** Movement = PLAYER_SPEED × delta_time

### Resize Handling
- **File changed:** `tty_invaders/game.py`
- **Implementation:** Tracks terminal width/height each frame
- **Behavior:** Triggers clean redraw when size changes

### Color Updates
- **File changed:** `tty_invaders/renderer/ui.py`
- **High score color:** `bright_yellow` (was `white`)
- **Score/Lives color:** `bright_white` (was `white`)

## How to Update

If you already have the game installed:
```bash
cd tty-invaders
git pull  # or download latest version
uv sync
uv run tty-invaders
```

## Testing

All 38 unit tests still pass after these changes:
```bash
uv run pytest tests/ -v
```

## Feedback

These improvements were made based on user feedback. If you have more suggestions, please let us know!
