# TTY Invaders - Game Balance Guide

## Current Balance (v1.0.2)

### Player Stats
- **Movement Speed**: 60 chars/sec
- **Shoot Cooldown**: 0.3 seconds (can fire ~3.3 shots/sec)
- **Lives**: 3
- **Bullet Speed**: 40 chars/sec (upward)

### Alien Stats by Level

| Level | Alien Speed | Shoot Frequency | Rows | Difficulty |
|-------|-------------|-----------------|------|------------|
| 1     | 5.0 c/s     | Every 2.5s      | 5    | Easy       |
| 2     | 6.5 c/s     | Every 2.35s     | 5    | Easy       |
| 3     | 8.0 c/s     | Every 2.2s      | 6    | Medium     |
| 4     | 9.5 c/s     | Every 2.05s     | 6    | Medium     |
| 5     | 11.0 c/s    | Every 1.9s      | 7    | Hard       |
| 10    | 18.5 c/s    | Every 1.4s      | 7    | Very Hard  |

### Speed Ratios (Player vs Aliens)

| Level | Player Speed | Alien Speed | Ratio | Player Advantage |
|-------|--------------|-------------|-------|------------------|
| 1     | 60 c/s       | 5.0 c/s     | 12:1  | Huge            |
| 2     | 60 c/s       | 6.5 c/s     | 9:1   | Very Large      |
| 3     | 60 c/s       | 8.0 c/s     | 7.5:1 | Large           |
| 5     | 60 c/s       | 11.0 c/s    | 5.5:1 | Moderate        |
| 10    | 60 c/s       | 18.5 c/s    | 3.2:1 | Small           |

### Shield Stats
- **Count**: 4 shields
- **Health**: 10 hits each
- **Position**: Between player and aliens
- **Degradation**: Visual damage shown at 75%, 50%, 25% health

### Scoring
- **Top Row Aliens** (red): 30 points
- **Middle Rows** (yellow): 20 points
- **Bottom Rows** (cyan): 10 points
- **Total Level 1**: 11 aliens × [varies] = ~220 points max

## Balance Philosophy

### Level 1 Design Goals
✅ **Beginner-Friendly**: Slow alien movement (5 c/s) gives new players time to learn controls
✅ **Safe Practice**: 2.5s between alien shots allows dodging practice
✅ **Room for Error**: Player moves 12× faster than aliens
✅ **Shield Protection**: 4 shields with 10 health each provide ample defense

### Difficulty Curve
- **Levels 1-2**: Learning phase - aliens very slow
- **Levels 3-4**: Skill building - moderate challenge
- **Levels 5+**: Expert play - requires good reflexes and strategy

### Challenge Increases Via
1. **Speed**: Aliens move faster (+1.5 c/s per level)
2. **Fire Rate**: Aliens shoot more often (-0.15s per level)
3. **Quantity**: More rows appear (max 7 rows by level 5)
4. **Chaos**: More aliens = more bullets to dodge

## Player Feedback Integration

### Recent Changes
- **v1.0.1**: Doubled player speed (30 → 60 c/s) for better responsiveness
- **v1.0.2**: Halved alien speed in level 1 (10 → 5 c/s) after feedback

### Result
The game now has a gentle learning curve while maintaining exciting gameplay in later levels.

## Tips for Players

**Level 1 Strategy:**
- Take your time - aliens move slowly
- Use shields as cover
- Focus on accuracy over speed
- Learn the timing of alien shots

**Advanced Strategy:**
- Clear bottom rows first (aliens descend when they reach edges)
- Save shields for later when bullets are more frequent
- Create "safe lanes" by clearing vertical columns
- Dodge rather than hide once shields are gone

## Tuning Notes

If you want to adjust difficulty, edit `tty_invaders/config.py`:

```python
# Easier
ALIEN_BASE_SPEED = 4          # Even slower start
ALIEN_SPEED_INCREMENT = 1.0   # Gentler progression

# Harder
ALIEN_BASE_SPEED = 7          # Faster start
ALIEN_SPEED_INCREMENT = 2.0   # Steeper progression
```
