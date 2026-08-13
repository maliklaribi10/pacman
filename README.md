*This activity has been created as part of the 42 curriculum by malaribi, comoulin.*

# Pac-Man

## Description

Pac-Man is a recreation of the famous arcade game originally released by Namco.

The goal of this activity is to create a complete and playable Pac-Man game in Python, using object-oriented programming, a graphical library, modular code and an external maze generator.

The game includes:

* A main menu
* Multiple procedurally generated levels
* Pac-Man movement and collision management
* Four different ghosts
* Pacgums and super-pacgums
* Score management
* Lives management
* A level timer
* Pause and resume functionality
* Game Over and Victory screens
* A persistent Top 10 highscore system
* A configurable game through a JSON configuration file
* A cheat mode for peer review
* A project management system based on a Kanban board

The project is written in Python and uses Pygame for the graphical part of the game.

---

## Features

### Player

Pac-Man can move through the maze using:

* `W`, `A`, `S`, `D`
* Arrow keys

The player can only move through corridors and cannot cross walls.

Pac-Man loses a life when touched by a ghost and respawns in the middle of the maze.

A level is completed when all pacgums have been eaten.

The game is completed when all levels have been completed.

### Ghosts

The game contains four ghosts:

* Blue
* Orange
* Pink
* Red

Ghosts move autonomously through the maze.

When they are not edible, they chase the player.

When Pac-Man eats a super-pacgum, ghosts become edible for a limited amount of time.

When an edible ghost is eaten, the player receives additional points.

### Pacgums

Pacgums are distributed throughout the maze.

Eating a normal pacgum increases the player's score.

Super-pacgums are placed in the corners of the maze. Eating one gives additional points and temporarily makes ghosts edible.

### Levels

The game contains 10 levels.

The first maze is generated using the configured seed. Subsequent levels use maze generation through the assigned A-Maze-ing package.

Each level has a time limit.

The player keeps their score and remaining lives when moving from one level to the next.

### Pause

Press `Escape` during a game to pause it.

The pause menu allows the player to:

* Resume the game
* Return to the main menu

### Cheat Mode

A cheat mode is available to make peer review easier.

Press `Ctrl` to activate the cheat mode.

Once cheat mode is activated, pressing `P` allows the player to immediately skip the current level.

This feature is intended to help reviewers quickly access and test different levels and game features.

---

# Instructions

## Requirements

The project requires:

* Python 3.10 or later
* Pygame
* The provided `mazegenerator` package

The project also uses Python type hints and is intended to follow the project's linting requirements using Flake8 and Mypy.

A virtual environment is recommended for installing the project's dependencies.

## Installation

Install the required dependencies using the project's package configuration and the provided maze generator package.

The A-Maze-ing package provided for this project is:

`mazegenerator-2.1.0-py3-none-any.whl`

The maze generator is used as an external dependency and is not modified by the project.

## Running the game

The game must be launched from the command line with exactly one configuration file:

```bash
python3 pac-man.py config.json
```

The configuration file must be a JSON file.

The program handles configuration errors without displaying a Python traceback.

---

# Controls

| Key       | Action                                           |
| --------- | ------------------------------------------------ |
| `W` / `↑` | Move up                                          |
| `A` / `←` | Move left                                        |
| `S` / `↓` | Move down                                        |
| `D` / `→` | Move right                                       |
| `Escape`  | Pause / resume                                   |
| `Ctrl`    | Activate cheat mode                              |
| `P`       | Skip the current level when cheat mode is active |

---

# Configuration

The game uses a JSON configuration file.

The current configuration contains the following parameters:

| Key                  |    Current value | Description                                  |
| -------------------- | ---------------: | -------------------------------------------- |
| `highscore_filename` | `highscore.json` | File used to store highscores                |
| `level`              |             `10` | Number of levels                             |
| `lives`              |              `1` | Number of player lives                       |
| `pacgum`             |              `1` | Pacgum configuration value                   |
| `score_pacgum`       |             `10` | Points awarded for eating a pacgum           |
| `score_superpacgum`  |             `50` | Points awarded for eating a super-pacgum     |
| `score_ghost`        |            `200` | Points awarded for eating an edible ghost    |
| `seed`               |             `42` | Seed used for maze generation                |
| `max_time`           |             `90` | Maximum time allowed for a level, in seconds |

Unknown configuration keys are ignored.

Invalid or missing configuration values are handled using safe values and clear error messages rather than Python tracebacks.

The configuration can be changed during the defense, so the game does not rely on hard-coded values for these parameters.

---

# Highscore

The game implements a persistent highscore system using a JSON file.

The highscore file is:

```text
highscore.json
```

The highscore system is updated whenever a player finishes a game and enters their name.

Highscores are loaded when the game starts and saved so that they remain available after the program is closed.

The highscore system is displayed from the main menu.

The project maintains the Top 10 scores.

Player names are limited to the format required by the activity, and scores are stored as non-negative integer values.

Using JSON keeps the system simple and makes the stored scores easy to read and update.

---

# Maze Generation

The maze generation is handled by the external A-Maze-ing package provided for the activity.

The project does not implement its own maze generator.

The provided package is installed as:

```text
mazegenerator-2.1.0-py3-none-any.whl
```

The maze generator is used without modifying the package.

The project's maze loading code adapts its own implementation to the interface provided by the package.

The configured seed is used for the initial maze generation, while subsequent levels can use randomly generated mazes.

The maze generator is configured to produce Pac-Man-compatible corridors.

If maze generation encounters an error, the game handles the error cleanly instead of crashing.

---

# Implementation

The project is implemented in Python using an object-oriented and modular approach.

The main entry point is:

```text
pac-man.py
```

The project also contains a dedicated character implementation:

```text
character.py
```

The graphical assets are organized in dedicated directories.

```text
d/
├── pac0.png
├── pac1.png
├── pac2.png
├── pac3.png
└── ghost/
    ├── blue/
    ├── orange/
    ├── pink/
    ├── red/
    └── scared/
```

Additional interface images are stored in:

```text
image/
├── bronze_medal.png
├── game_over.png
├── gold_medal.png
├── instruction.png
├── silver_medal.png
└── victory.png
```

The project also includes a custom font:

```text
police/
└── Pixeltype.ttf
```

The configuration and persistent data are stored separately:

```text
config.json
highscore.json
```

---

# General Software Architecture

The project is organized around the different responsibilities of the game.

## Main program

`pac-man.py`

This is the main entry point of the application.

It is responsible for starting the game, loading the configuration and managing the different states of the game.

## Character management

`character.py`

This module contains character-related functionality used by the game, including player and/or character behavior.

## Configuration

`config.json`

Contains configurable gameplay parameters such as:

* Number of levels
* Number of lives
* Scores
* Maze seed
* Level timer
* Highscore filename

## Highscore

`highscore.json`

Stores persistent player scores.

## Assets

The project separates visual resources from the Python source code.

This makes it possible to modify sprites, screens and fonts without changing the main game logic.

## Project structure

```text
.
├── character.py
├── config.json
├── highscore.json
├── pac-man.py
├── Makefile
├── pyproject.toml
├── d/
│   ├── pac0.png
│   ├── pac1.png
│   ├── pac2.png
│   ├── pac3.png
│   └── ghost/
│       ├── blue/
│       ├── orange/
│       ├── pink/
│       ├── red/
│       └── scared/
├── image/
│   ├── bronze_medal.png
│   ├── game_over.png
│   ├── gold_medal.png
│   ├── instruction.png
│   ├── silver_medal.png
│   └── victory.png
└── police/
    └── Pixeltype.ttf
```

---

# User Interface

## Main Menu

The main menu provides access to the main game features:

* Start Game
* Highscores
* Instructions
* Exit

The highscore list is accessible from the main menu.

## In-Game HUD

During gameplay, the interface displays the main game information, including:

* Current score
* Remaining lives
* Current level
* Remaining time

## Pause Menu

The pause menu allows the player to:

* Resume the game
* Return to the main menu

## Game Over

When the player loses all available lives, the Game Over screen is displayed.

The final score is shown and the player can enter their name to save their score.

## Victory

When all levels are completed, the Victory screen is displayed.

The final score is shown and the player can enter their name to save their score.

---

# Project Management

The project was managed using a Kanban board.

The board was used to divide the project into different tasks and track their completion.

The completed tasks included:

* Collision management
* Pac-Man movement
* Ghost movement
* Score, lives, timer and level management
* Game Over and Victory screens
* Highscore management and score saving
* Main menu management
* Makefile implementation
* Configuration file management
* README creation

The Kanban approach allowed the team to divide the work into specific features and track the progress of the activity.

The project was developed by:

* `malaribi`
* `comoulin`

---

# Testing

No dedicated testing framework such as `pytest` or `unittest` was used for this project.

The game was tested manually during development by running the different game features and checking their behavior.

The main features checked include:

* Player movement
* Collision handling
* Ghost movement
* Pacgum collection
* Super-pacgum behavior
* Score calculation
* Lives
* Level progression
* Timer
* Pause
* Game Over
* Victory
* Highscore saving
* Configuration loading
* Cheat mode

---

# AI Usage

AI tools were used as a learning and documentation aid during the development of the project.

AI was mainly used for:

* Explaining Pygame concepts and mechanisms
* Helping understand how certain graphical game features work
* Assisting with the preparation and structure of this README

AI-generated information was used as an explanation and learning resource. The developers remained responsible for understanding and implementing the project.

The project follows the principle that AI-generated content should only be used when the developers understand it and can explain their implementation during peer review.

---

# Makefile

A Makefile is included in the repository.

The Makefile is currently still being finalized.

The intended Makefile commands follow the activity requirements:

```text
make install
make run
make debug
make clean
make lint
```

The `lint` rule is intended to run both Flake8 and Mypy with the required options.

Once the Makefile is finalized, it will provide a convenient way to install dependencies, launch the game, debug the program, clean generated files and verify the code quality.

---

# Resources

The following resources were used as references during the development of the project:

* Python documentation
* Pygame documentation
* PEP 8 / Flake8 documentation
* Mypy documentation
* PEP 257 documentation for Python docstrings
* Documentation and interface provided with the A-Maze-ing package
* The official 42 Pac-Man activity subject

AI tools were also used to explain Pygame concepts and assist with README preparation, as described in the **AI Usage** section.

---

# Project Packaging

A COMPLETER
---