import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass, field
from typing import List
from config import (
    bot_n, bot_aggro, p_bombs,
    p_power, tick, bot_v
)


@dataclass
class GameSet:
    bots: int = bot_n
    aggro: float = bot_aggro
    pl_b_max: int = p_bombs
    pl_b_pow: int = p_power
    tick_ms: int = tick
    vis: int = bot_v
    pathfinding_algorithm: str = 'a_star'
    heuristic: str = 'manhattan'
    available_algorithms: List[str] = field(default_factory=lambda: ['a_star', 'dijkstra', 'bfs'])
    available_heuristics: List[str] = field(default_factory=lambda: ['manhattan', 'euclidean', 'chebyshev'])

class SetScreen(tk.Frame):
    def __init__(self, root, init_set: GameSet, start_cb):
        super().__init__(root, bg="#222", padx=20, pady=20)
        self.start_cb = start_cb
        self.settings = init_set

        tk.Label(self, text="Bomberman Settings", font=("Consolas", 24, "bold"), bg="#222", fg="#eee").pack(pady=(0, 25))

        self.entries = {}
        
        self.entries['tick_ms'] = self.mk_entry("Game Speed (ms tick)", self.settings.tick_ms, "Lower is Faster")
        self.entries['bots'] = self.mk_entry("Bot Count", self.settings.bots)
        self.entries['aggro'] = self.mk_entry("Bot Aggression", self.settings.aggro, "Chance to bomb (0.1 to 1.0)")
        self.entries['pl_b_max'] = self.mk_entry("Player Start Bombs", self.settings.pl_b_max)
        self.entries['pl_b_pow'] = self.mk_entry("Player Start Power", self.settings.pl_b_pow)

        self.algorithm_var = tk.StringVar(value=self.settings.pathfinding_algorithm)
        self.heuristic_var = tk.StringVar(value=self.settings.heuristic)

        self.mk_dropdown("Pathfinding Algorithm", self.algorithm_var, self.settings.available_algorithms, self.on_algorithm_change)
        self.heuristic_dropdown = self.mk_dropdown("Heuristic (for A*)", self.heuristic_var, self.settings.available_heuristics)

        self.err_lbl = tk.Label(self, text="", font=("Consolas", 12), bg="#222", fg="#ff5555")
        self.err_lbl.pack(pady=(10, 0))

        tk.Button(self, text="Start Game", command=self.start,
                  font=("Consolas", 16, "bold"), bg="#4f4", fg="#111",
                  relief="flat", pady=10).pack(pady=(20, 0), fill="x")
        
        self.on_algorithm_change()

    def mk_entry(self, text, default, desc=None):
        frame = tk.Frame(self, bg="#222")
        
        lbl_txt = f"{text}:"
        label = tk.Label(frame, text=lbl_txt, font=("Consolas", 12), anchor="w", width=25, bg="#222", fg="#ddd")
        label.pack(side="left", padx=(0, 10))

        e_var = tk.StringVar(value=str(default))
        entry = tk.Entry(frame, textvariable=e_var, width=10,
                         font=("Consolas", 12), bg="#444", fg="#eee",
                         relief="flat", insertbackground="#eee")
        entry.pack(side="left", fill="x", expand=True)

        if desc:
            tk.Label(frame, text=desc, font=("Consolas", 9), anchor="w", bg="#222", fg="#999").pack(side="left", padx=(10, 0))

        frame.pack(fill="x", pady=8)
        return e_var

    def mk_dropdown(self, text, var, options, command=None):
        frame = tk.Frame(self, bg="#222")
        
        label = tk.Label(frame, text=f"{text}:", font=("Consolas", 12), anchor="w", width=25, bg="#222", fg="#ddd")
        label.pack(side="left", padx=(0, 10))

        dropdown = ttk.Combobox(frame, textvariable=var, values=options, state="readonly",
                                font=("Consolas", 12))
        dropdown.pack(side="left", fill="x", expand=True)
        if command:
            dropdown.bind("<<ComboboxSelected>>", command)

        frame.pack(fill="x", pady=8)
        return dropdown

    def on_algorithm_change(self, event=None):
        if self.algorithm_var.get() == 'a_star':
            self.heuristic_dropdown.config(state="readonly")
        else:
            self.heuristic_dropdown.config(state="disabled")

    def start(self):
        try:
            s = GameSet(
                bots=int(self.entries['bots'].get()),
                aggro=float(self.entries['aggro'].get()),
                pl_b_max=int(self.entries['pl_b_max'].get()),
                pl_b_pow=int(self.entries['pl_b_pow'].get()),
                tick_ms=int(self.entries['tick_ms'].get()),
                pathfinding_algorithm=self.algorithm_var.get(),
                heuristic=self.heuristic_var.get()
            )
            s.aggro = max(0.0, min(1.0, s.aggro))
            
            self.err_lbl.config(text="")
            self.start_cb(s)
        
        except ValueError:
            self.err_lbl.config(text="Invalid input. Please enter valid numbers.")
        except Exception as e:
            self.err_lbl.config(text=f"An error occurred: {e}")
