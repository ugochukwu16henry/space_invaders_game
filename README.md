# Space Invaders Game

This project is a Space Invaders-style arcade game built with Python and the Arcade library. You control a ship at the bottom of the screen, shoot enemy waves, protect your remaining lives, and advance through harder levels as the game speeds up.

## What To Install

You need the following before starting the game:

- Python 3.10 or newer
- The Python package listed in `requirements.txt`

Install the dependency with:

```bash
pip install -r requirements.txt
```

The current required package is:

- `arcade>=2.6.17`

If you want isolated dependencies, create and activate a virtual environment first.

## How To Start The Game

From the project folder, run:

```bash
python main.py
```

If you are using a virtual environment, activate it before running the command.

## How To Play

Your goal is to destroy all enemies before they reach your ship or remove all of your lives.

### Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Fire a shot
- Enter: Start the game or restart after game over
- F5: Save the current game
- F9: Load the saved game

### Rules

- Destroy every enemy ship to clear the current wave.
- Each enemy you destroy adds points to your score.
- New levels add more enemies and increase difficulty.
- You lose a life when an enemy bullet hits your ship.
- The game ends when your lives reach zero.
- The game also ends if the enemy formation reaches your ship.

## Project Overview

This project was built to strengthen practical software engineering skills through real-time input handling, collision systems, asset integration, save/load support, and interactive game-loop design.

Features included in the current version:

- Start screen with controls and rules
- Player movement and shooting
- Enemy wave spawning and level progression
- Score and lives tracking
- Save and load support
- Sound effects and background music
- Game over screen

## Development Environment

This project was developed in Visual Studio Code on Windows using Python and a virtual environment.

Tools and technologies used:

- Visual Studio Code
- Python 3
- Arcade
- Pyglet
- Git and GitHub

## Useful Websites

- [Arcade Documentation](https://api.arcade.academy/en/latest/)
- [Python Official Documentation](https://docs.python.org/3/)
- [Pyglet Documentation](https://pyglet.readthedocs.io/en/latest/)

## Future Work

- Add animated sprites and explosion effects.
- Replace repeated `draw_text` calls with cached `Text` objects.
- Add power-ups, enemy variety, and a persistent high-score system.
