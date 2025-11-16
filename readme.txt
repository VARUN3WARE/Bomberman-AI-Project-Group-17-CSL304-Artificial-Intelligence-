Bomberman (Tkinter) - Project README

This document provides a detailed breakdown of the Bomberman game, its core features, AI logic, and file structure.

=========================
Core Features & Gameplay
=========================

This is a classic Bomberman game implemented in Python using the Tkinter library. The player controls a character that can place bombs to destroy soft walls and defeat enemies. The goal is to be the last one standing.

- Player Control: The player can move up, down, left, or right, and place bombs.
- Bots: The game features AI-controlled bots that navigate the map, place bombs, and hunt the player.
- Destructible Environment: The map contains soft walls that can be destroyed by bombs.
- Win/Loss Conditions: The game ends when either the player is defeated (loss) or all bots are defeated (win).

================
AI and Bot Logic
================

The bot AI is the most complex part of the game. It is designed to be challenging and dynamic, with several layers of logic governing its behavior.

--------------------
1. State Machine
--------------------

Each bot operates on a simple state machine that dictates its primary objective at any given moment. The states are:

- `search`: This is the default state. The bot will look for the nearest soft wall to destroy. The goal is to clear the map and find the player.
- `chase`: If the player comes within the bot's `vision` range, the bot will switch to this state. Its target becomes the player's current position, and it will actively hunt the player.
- `evade`: This state has the highest priority. If a bot detects that it is in the blast radius of a bomb that is about to explode, it will immediately switch to this state to find a safe tile.

--------------------
2. Pathfinding (A* Algorithm)
--------------------

Bots use the A* (A-star) pathfinding algorithm to navigate the map.

- Heuristic: The A* algorithm requires a heuristic to estimate the distance to the target. This game uses the **Manhattan distance**, which is the sum of the absolute differences of the x and y coordinates. It's a fast and effective heuristic for grid-based games.
- `pathfinding.py`: This file contains the `a_star` function, which takes the game map, a start position, and a goal position, and returns the optimal path (a list of coordinates).
- Forbidden Tiles: The A* implementation can also take a set of "forbidden" tiles that the bot is not allowed to enter.

--------------------
3. Priority Movement & Evasion
--------------------

A bot's movement is not just about following a path. It also involves making smart decisions to stay alive.

- **Myopic Evasion Fix**: A simple evasion logic might just find the nearest safe tile. However, that tile could be a dead end. The AI in this game has been improved to address this "myopic" (short-sighted) evasion.
  - When a bot needs to evade, it performs a search for up to 5 of the nearest safe tiles.
  - It then scores these candidate tiles based on their "openness" (the number of walkable neighbors).
  - The bot chooses the path to the safe tile with the best score, prioritizing openness over raw distance. This makes it more likely to escape to an open area rather than a corner.

- **Bomb Placement Safety Check**: A bot will not place a bomb unless it is sure it can escape the blast.
  - The `bot_can_escape_after_placing` function simulates placing a bomb and then performs a search to see if a safe tile is reachable within the bomb's fuse time.
  - This prevents bots from trapping themselves, making them much more intelligent.

- **Path Interruption**: If a bot is following a path and a step on that path suddenly becomes dangerous (e.g., another bot places a bomb), it will clear its current path and recalculate on the next tick.

=================================
Game Settings and Their Influence
=================================

The `settings.py` file allows you to customize the game, and these settings have a significant impact on gameplay and bot behavior.

- `bot_aggression` (0.1 to 1.0): This is a crucial setting that controls how likely a bot is to place a bomb when it is in the `chase` state and near the player.
  - A low value (e.g., 0.2) will make bots more hesitant, giving the player more breathing room.
  - A high value (e.g., 0.8) will make bots very aggressive, placing bombs almost as soon as they get close to the player.

- `bot_vision` (integer): This determines the distance (in tiles) a bot can "see." If the player enters this range, the bot will switch from `search` to `chase`.
  - A smaller vision range makes it easier for the player to sneak around the map.
  - A larger vision range makes bots more aware and relentless.

- `game_tick_ms` (milliseconds): This controls the main game loop speed. A lower value makes the entire game faster (player movement, bot movement, bomb fuses).

- `player_max_bombs` & `player_bomb_power`: These settings control the player's starting abilities, allowing you to make the game easier or harder for the player.

===============
File Breakdown
===============

- `main.py`: The entry point of the application. It handles the main window, and switches between the settings screen and the game screen.

- `config.py`: Contains all the core constants of the game, such as window dimensions, map size, tile types, and default game settings like bomb fuse time and player health.

- `settings.py`: Defines the `GameSettings` data class and the `SettingsScreen` UI. This allows the player to configure game variables before starting.

- `game.py`: This is the heart of the game. The `Game` class manages the main game loop (`tick`), entities (player, bots), bombs, and explosions. It handles player input, AI updates, drawing everything on the canvas, and checking for win/loss conditions.

- `entities.py`: Defines the data structures for all game objects using Python's `dataclass`. This includes `Player`, `Computer` (the bot), `Bomb`, `Explosion`, and `Tile`.

- `map.py`: Contains the `GameMap` class, which is responsible for generating the game world, including the hard and soft walls. It also provides helper methods like `is_walkable`.

- `pathfinding.py`: Implements the A* pathfinding algorithm used by the bots to navigate the game world.

- `utils.py`: A collection of utility functions, such as `now_ms()` to get the current time in milliseconds and `manhattan()` for the A* heuristic.
