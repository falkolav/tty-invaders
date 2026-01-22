# Sound Effects Directory

This directory contains the retro sound effects for TTY Invaders.

## Current Sound Files

The following classic Space Invaders sounds are included:

- `shoot.wav` - Player shooting sound
- `invaderkilled.wav` - Alien explosion sound
- `fastinvader1.wav` - Heartbeat sound (slow)
- `fastinvader2.wav` - Heartbeat sound (medium)
- `fastinvader3.wav` - Heartbeat sound (fast)
- `fastinvader4.wav` - Heartbeat sound (fastest)
- `ufo_lowpitch.wav` - UFO sound (low pitch)
- `ufo_highpitch.wav` - UFO sound (high pitch)

## Custom Sound Files

You can replace these with your own custom sound effects:

- Format: WAV files
- Recommended: 22050 Hz, 16-bit, mono or stereo
- Keep files small for quick loading (under 100KB recommended)

## Fallback Behavior

If pygame-ce fails to initialize or sound files are missing, the game will gracefully fall back to using the terminal bell (`\a`) for sound effects.

## Creating Retro Sounds

You can create retro-style sound effects using:
- Online generators: sfxr, bfxr, ChipTone
- Python libraries: pydub, scipy
- Audio editing: Audacity with 8-bit/chiptune effects

## Disabling Sounds

Sounds can be toggled on/off in the game's Options menu.
