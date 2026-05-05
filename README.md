# Word Runner

A maze-based typing game built with Python and Pygame.

## Team
- FourRunner
- Emily Tinajero
- Saif Majali
- Yu Ting Keung
- Nathan Choi

## Overview
Word Runner combines maze exploration with typing accuracy. From the player’s current cell, each valid move direction shows a random 5-letter word on the adjacent tile. The player types the word letter by letter to move in that direction.

## Gameplay
- Start inside a generated maze.
- Each open direction (up/down/left/right) has a random 5-letter word.
- Type the displayed word one letter at a time.
- Correct letters advance progress.
- Mistakes reset progress and apply a short penalty.
- Complete a word to move into that tile.
- Reach the exit to win.

## Controls
- Type letters to select and complete a direction word
- `Esc`: cancel the current word selection
- After winning:
  - `R`: restart the game
  - `Q`: quit

## Requirements
- Python 3.12
- Pygame

## Installation
1. Install Python 3.12.
2. Install Pygame:
   ```bash
   py -3.12 -m pip install pygame
   ```

## Run
```bash
py -3.12 main.py
```

## Project files
- `main.py` — game loop and input handling
- `maze.py` — maze generation and movement logic
- `render.py` — graphics and HUD rendering
- `word.py` — word loading and assignment
- `Scoreboard.py` — score saving and loading
- `dictionary.txt` — word list source
- `scores.json` — stored score data

## Notes
This README can also be extended with screenshots, a short demo GIF, or a known issues / future improvements section.
