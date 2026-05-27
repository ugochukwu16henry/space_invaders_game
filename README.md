Overview

This project was built to strengthen my practical software engineering skills by designing, implementing, testing, and iterating on a complete game loop in Python. My goal was to improve at real-time input handling, collision systems, asset integration, and debugging interactive applications.

I created a Space Invaders-style arcade game where the player controls a ship at the bottom of the screen and fights descending enemy waves. The player moves with the arrow keys, fires with the space bar, and progresses through increasingly difficult levels as enemy count and speed scale up. The game includes score tracking, lives, level progression, sound effects, background music, a start screen, and a game over screen.

My purpose for writing this software was to gain hands-on experience building a small but complete interactive system from scratch. I wanted to practice structuring game code into update loops and helper methods, handling edge cases across different library versions, and integrating media assets while keeping reliable gameplay behavior.

I will add my demonstration link after recording a 4-5 minute walkthrough showing gameplay and key code sections.

[Software Demo Video](http://youtube.link.goes.here)

## Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Shoot
- Enter: Start game / Restart
- F5: Save game
- F9: Load saved game

# Development Environment

I developed this project in Visual Studio Code on Windows using a Python virtual environment for dependency isolation.

Tools and technologies used:
- Visual Studio Code
- Python 3
- Arcade library (2D game framework)
- Pyglet (used by Arcade for rendering/audio)
- Git and GitHub for version control

# Useful Websites

The following resources were helpful while building and troubleshooting the game:
* [Arcade Documentation](https://api.arcade.academy/en/latest/)
* [Python Official Documentation](https://docs.python.org/3/)
* [Pyglet Documentation](https://pyglet.readthedocs.io/en/latest/)

# Future Work

Planned improvements for future versions:
* Add animated sprites and explosion effects for more visual feedback.
* Replace draw_text calls with cached Text objects for better performance.
* Add power-ups, enemy variety, and a persistent high-score system.
