# Space Invaders Game (Arcade)

A Space Invaders-style game built with Python and Arcade.

## Module Requirements Coverage

- Graphics display: Player, enemies, bullets, HUD, start/game-over screens.
- User input: Keyboard controls for movement, shooting, and restart.
- Moveable objects: Player ship, enemy wave, player bullets, enemy bullets.
- Additional requirement: Levels increase game difficulty (faster and larger waves).
- Extra feature: Sound effects for shooting, enemy hits, and game over.

## Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Fire bullet
- Enter: Start game / Restart after game over

## Setup

1. Install Python (3.10+ recommended).
2. Install Arcade:

```bash
pip install arcade
```

3. Run the game:

```bash
python main.py
```

## Optional Assets

- You can add your own sounds in `sounds/`:
  - `sounds/shoot.wav`
  - `sounds/explode.wav`
  - `sounds/game_over.wav`

If these files are not present, built-in Arcade sounds are used automatically.

## Gameplay Rules

- Destroy enemies to increase your score.
- Each level increases enemy count and speed.
- You lose a life if hit by enemy fire.
- Game ends when lives reach zero or enemies reach your ship.
