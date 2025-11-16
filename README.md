# 🎮 Bomberman (Tkinter) – AI Project README

A complete breakdown of the Bomberman AI project, including gameplay features, AI logic, and file structure.

---

## ⭐ Overview

This is a classic **Bomberman game** implemented in **Python (Tkinter)** with intelligent AI-controlled bots.  
The player and bots move around a destructible grid environment, placing bombs, avoiding explosions, and trying to be the last one alive.

---

# 🎬 Project Demo Video

## 📌 YouTube Link

Watch the full gameplay demo here:  
👉 **https://www.youtube.com/watch?v=fGdCZeGzFvk**

---

<!-- ## 🎬 Embedded Gameplay Demo (Directly Playable)

<p align="center">
  <video width="70%" controls>
    <source src="https://raw.githubusercontent.com/VARUN3WARE/Bomberman-AI-Project-Group-17-CSL304-Artificial-Intelligence-/main/assets/bombermanai.mp4" type="video/mp4">
    Your browser does not support the video tag. You can download the video directly from the repo: [assets/bombermanai.mp4](assets/bombermanai.mp4)
  </video>
</p>

--- -->

# 🔥 Core Features & Gameplay

This project recreates the traditional Bomberman experience with added AI enhancements.

### ▶️ Player Controls

- Move: Up, Down, Left, Right
- Drop bombs to destroy soft walls and enemies

### 🤖 AI Bots

- Navigate the grid intelligently
- Place bombs strategically
- Avoid explosions
- Hunt down the player

### 🧱 Destructible Environment

- Soft walls can be destroyed by bombs
- Hard walls remain indestructible

### 🏆 Win/Loss Conditions

- **Win:** All bots defeated
- **Lose:** Player runs out of HP or gets caught in an explosion

---

# 🧠 AI and Bot Logic

The AI system is the heart of this game. It uses a layered approach with a state machine, A\* pathfinding, evasion scoring, and safety checks.

---

## 1️⃣ State Machine

Every bot operates on 3 core states:

### 🔹 `search` (Default)

Bot searches for soft walls to destroy while exploring the map.

### 🔹 `chase`

Triggered when bot detects the player within its **vision** range.  
Bot actively moves towards the player.

### 🔹 `evade` (Highest Priority)

Activated when bot detects danger (bomb blast radius).  
Bot immediately searches for safe tiles.

---

## 2️⃣ Pathfinding – A\* Algorithm

Bots use **A\*** to navigate the map efficiently.

- **Heuristic:** Manhattan distance
- Pathfinding implemented in: `pathfinding.py`
- Supports:
  - Avoiding bombs
  - Avoiding dangerous tiles
  - Avoiding forbidden zones

The algorithm returns an **optimal path** from start → target.

---

## 3️⃣ Intelligent Movement & Evasion

### ✔ Improved Myopic Evasion Fix

Bots:

1. Identify **up to 5 nearest safe tiles**
2. Evaluate each tile based on **openness** (number of walkable neighbors)
3. Choose the safest + most open tile
4. Navigate toward it

This prevents bots from running into dead ends.

### ✔ Bomb Placement Safety Check

Bots simulate future states using:

> `bot_can_escape_after_placing()`

Before placing a bomb, they check if they can escape before it explodes.

### ✔ Path Interruption

If a path becomes unsafe (bomb placed mid-route), bot cancels the path and recalculates.

---

# ⚙️ Game Settings & Their Impact

The `settings.py` file allows customization of gameplay and AI behavior.

### 🔸 `bot_aggression` (0.1 → 1.0)

Controls how frequently bots place bombs when chasing.

- Low = cautious bots
- High = extremely aggressive bots

### 🔸 `bot_vision`

How far bots can “see” the player (in tiles).

### 🔸 `game_tick_ms`

Controls game speed. Lower = faster gameplay.

### 🔸 `player_max_bombs` / `player_bomb_power`

Tune difficulty for the player.

---

## 📁 File structure

Here's a compact, easy-to-scan overview of the repository root and what each file/folder does. Filenames are wrapped in backticks — click to open them on GitHub.

```
.
├── assets/                 # media (sprites, demo video)
│   └── bombermanai.mp4
├── botai.txt               # AI notes / logs
├── config.py               # constants and global config
├── entities.py             # Player, Bot, Bomb, Explosion dataclasses
├── game.py                 # core game loop and rendering
├── main.py                 # UI entry point and game launcher
├── map.py                  # map generation & tile logic
├── pathfinding.py          # A* pathfinding implementation
├── README.md               # this file
├── settings.py             # game settings & settings UI
├── utils.py                # small helper utilities
└── __pycache__/            # Python bytecode (ignored in VCS)
```
