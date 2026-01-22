# Valid Blessed Terminal Colors

This document lists the valid color names for the blessed terminal library used in TTY Invaders.

## Basic Colors
- `black`
- `red`
- `green`
- `yellow`
- `blue`
- `magenta`
- `cyan`
- `white`

## Bright Colors
- `bright_black` (displays as gray)
- `bright_red`
- `bright_green`
- `bright_yellow`
- `bright_blue`
- `bright_magenta`
- `bright_cyan`
- `bright_white`

## Colors Used in TTY Invaders

### From config.py
- Player: `green`
- Alien (top row): `red`
- Alien (middle rows): `yellow`
- Alien (bottom rows): `cyan`
- Player bullet: `white`
- Alien bullet: `red`
- Shield: `blue`
- UI: `white`
- Menu: `cyan`
- Explosion: `yellow`

### From UI files
- Menu title: `bright_cyan`
- Selected option: `bright_white`
- Footer text: `bright_black` (gray)
- Game over: `red`
- High score: `yellow`

## Note
`dark_gray` is NOT a valid blessed color. Use `bright_black` instead for gray text.
