# Pacman Game

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [1. Clone or download the repository](#1-clone-or-download-the-repository)
  - [2. Install dependencies](#2-install-dependencies)
- [Running the Game](#running-the-game)
- [Game Controls](#game-controls)
- [Gameplay Features](#gameplay-features)
  - [Levels](#levels)
  - [Test Cases](#test-cases)
  - [Game Mechanics](#game-mechanics)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

## Overview

This is a Python implementation of the classic Pacman game featuring various AI algorithms for ghost movement. The game includes multiple levels with different AI behaviors and test cases for customizing gameplay scenarios.

## System Requirements

- Python 3.8 or higher
- Pygame 2.5.2
- Windows, macOS, or Linux operating system

## Installation

### 1. Clone or download the repository

Download and extract the project files to your local machine.

### 2. Install dependencies

Open a terminal/command prompt and navigate to the project directory:

- `cd path/to/project`
- `pip install -r requirements.txt`

## Running the Game

From the project's root directory, run:

`python main.py`

## Game Controls

- **Arrow Keys**: Move Pacman (in level 6 or playable levels)
- **ESC**: Return to the main menu at any time
- **Enter or ESC**: Restart game when on the game over screen

## Gameplay Features

### Levels

- **Levels 1-5**: Algorithm demonstration levels (Pacman can not move)
- **Level 6**: Playable level where you control Pacman

### Test Cases

After selecting a level, you can choose from 5 different test cases that modify the starting positions of Pacman and the ghosts. For levels 5-6, test case 6 is automatically selected.

### Game Mechanics

- Navigate Pacman through the maze to avoid ghosts.

## Project Structure

```
main.py                # Entry point of the game
requirements.txt       # Project dependencies
README.md              # Project documentation
.gitignore             # Git ignore configuration
|
|---- src/             # Main source code
|     |
|     |---- config.py  # Game configuration and constants
|     |---- runner.py  # Main game loop and initialization
|     |
|     |---- algorithm/ # AI algorithms for ghost movement
|     |     |---- AStar.py    # A* Search algorithm implementation
|     |     |---- BFS.py      # Breadth-First Search implementation
|     |     |---- DFS.py      # Depth-First Search implementation
|     |     |---- UCS.py      # Uniform Cost Search implementation
|     |
|     |---- game/      # Game logic and state management
|     |     |---- state_management.py    # Manages game state variables
|     |     |---- level_management.py    # Handles level loading
|     |     |---- event_management.py    # Processes game events and input
|     |
|     |---- gui/       # User interface and rendering
|     |     |---- menu.py               # Menu system and test case selector
|     |     |---- screen_management.py  # Screen display and transitions
|     |     |---- pacman_map.py         # Map rendering and management
|     |
|     |---- sprites/   # Game characters and objects
|     |     |---- pacman.py          # Pacman character implementation
|     |     |---- ghost.py           # Ghost characters and GhostManager
|     |     |---- sprite_configs.py  # Sprite configuration and paths
|     |
|     |---- utils/     # Utility functions and helpers
|           |---- algorithm_utils.py  # Common utilities for algorithms
|           |---- map_utils.py        # Map loading and processing
|           |---- movement_ultils.py  # Movement and collision detection
|           |---- screen_utils.py     # UI and performance metrics display
|
|---- map/             # Level and test case data
|     |---- pacman_map.json    # Main map configuration
|     |---- test_case_1.json   # Test case 1 positions
|     |---- test_case_2.json   # Test case 2 positions
|     |---- test_case_3.json   # Test case 3 positions
|     |---- test_case_4.json   # Test case 4 positions
|     |---- test_case_5.json   # Test case 5 positions
|     |---- test_case_6.json   # Test case 6 positions (for levels 5-6)
|
|---- assets/          # Game assets
      |---- ghosts/     # Ghost sprites
      |     |---- blinky.png    # Red ghost
      |     |---- clyde.png     # Orange ghost
      |     |---- inky.png      # Blue ghost
      |     |---- pinky.png     # Pink ghost
      |
      |---- map/        # Map tiles and elements
      |     |---- big_corner.png
      |     |---- door.png
      |     |---- (various map elements)
      |
      |---- pacman-down/  # Pacman animations facing down
      |---- pacman-left/  # Pacman animations facing left
      |---- pacman-right/ # Pacman animations facing right
      |---- pacman-stop/  # Pacman in stopped state
      |---- pacman-up/    # Pacman animations facing up
```

## Troubleshooting

If you encounter any issues:

1. Ensure Python and all dependencies are correctly installed.
2. Check that you're running the game from the project's root directory.
3. For rendering issues, ensure your system meets the minimum requirements for Pygame.

## Credits

This Pacman implementation was created as an AI course project, focusing on pathfinding and AI behavior algorithms.
