import tkinter as tk
from tkinter import ttk
<<<<<<< HEAD
from dataclasses import dataclass
=======
from dataclasses import dataclass, field
from typing import List
>>>>>>> origin/master
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
<<<<<<< HEAD
=======
    pathfinding_algorithm: str = 'a_star'
    heuristic: str = 'manhattan'
    available_algorithms: List[str] = field(default_factory=lambda: ['a_star', 'dijkstra', 'bfs'])
    available_heuristics: List[str] = field(default_factory=lambda: ['manhattan', 'euclidean', 'chebyshev'])
>>>>>>> origin/master

class SetScreen(tk.Frame):
    def __init__(self, root, init_set: GameSet, start_cb):
        super().__init__(root, bg="#222", padx=20, pady=20)
        self.start_cb = start_cb
<<<<<<< HEAD
        


=======
        self.settings = init_set
>>>>>>> origin/master

        tk.Label(self, text="Bomberman Settings", font=("Consolas", 24, "bold"), bg="#222", fg="#eee").pack(pady=(0, 25))

        self.entries = {}
        
<<<<<<< HEAD
        self.entries['tick_ms'] = self.mk_entry(
            "Game Speed (ms tick)", init_set.tick_ms, "Lower is Faster")
        
        self.entries['bots'] = self.mk_entry(
            "Bot Count", init_set.bots)
        
        self.entries['aggro'] = self.mk_entry(
            "Bot Aggression", init_set.aggro, "Chance to bomb (0.1 to 1.0)")


        self.entries['pl_b_max'] = self.mk_entry(
            "Player Start Bombs", init_set.pl_b_max)


        self.entries['pl_b_pow'] = self.mk_entry(
            "Player Start Power", init_set.pl_b_pow)

=======
        self.entries['tick_ms'] = self.mk_entry("Game Speed (ms tick)", self.settings.tick_ms, "Lower is Faster")
        self.entries['bots'] = self.mk_entry("Bot Count", self.settings.bots)
        self.entries['aggro'] = self.mk_entry("Bot Aggression", self.settings.aggro, "Chance to bomb (0.1 to 1.0)")
        self.entries['pl_b_max'] = self.mk_entry("Player Start Bombs", self.settings.pl_b_max)
        self.entries['pl_b_pow'] = self.mk_entry("Player Start Power", self.settings.pl_b_pow)

        self.algorithm_var = tk.StringVar(value=self.settings.pathfinding_algorithm)
        self.heuristic_var = tk.StringVar(value=self.settings.heuristic)

        self.mk_dropdown("Pathfinding Algorithm", self.algorithm_var, self.settings.available_algorithms, self.on_algorithm_change)
        self.heuristic_dropdown = self.mk_dropdown("Heuristic (for A*)", self.heuristic_var, self.settings.available_heuristics)
>>>>>>> origin/master

        self.err_lbl = tk.Label(self, text="", font=("Consolas", 12), bg="#222", fg="#ff5555")
        self.err_lbl.pack(pady=(10, 0))

<<<<<<< HEAD

        tk.Button(self, text="Start Game", command=self.start,
                  font=("Consolas", 16, "bold"), bg="#4f4", fg="#111",
                  relief="flat", pady=10).pack(pady=(20, 0), fill="x")

=======
        tk.Button(self, text="Start Game", command=self.start,
                  font=("Consolas", 16, "bold"), bg="#4f4", fg="#111",
                  relief="flat", pady=10).pack(pady=(20, 0), fill="x")
        
        self.on_algorithm_change()
>>>>>>> origin/master

    def mk_entry(self, text, default, desc=None):
        frame = tk.Frame(self, bg="#222")
        
        lbl_txt = f"{text}:"
<<<<<<< HEAD

        label = tk.Label(frame, text=lbl_txt, font=("Consolas", 12), anchor="w", width=25, bg="#222", fg="#ddd")
        label.pack(side="left", padx=(0, 10))

        
        e_var = tk.StringVar(value=str(default))
        entry = tk.Entry(frame, textvariable=e_var, width=10,

=======
        label = tk.Label(frame, text=lbl_txt, font=("Consolas", 12), anchor="w", width=25, bg="#222", fg="#ddd")
        label.pack(side="left", padx=(0, 10))

        e_var = tk.StringVar(value=str(default))
        entry = tk.Entry(frame, textvariable=e_var, width=10,
>>>>>>> origin/master
                         font=("Consolas", 12), bg="#444", fg="#eee",
                         relief="flat", insertbackground="#eee")
        entry.pack(side="left", fill="x", expand=True)

<<<<<<< HEAD

=======
>>>>>>> origin/master
        if desc:
            tk.Label(frame, text=desc, font=("Consolas", 9), anchor="w", bg="#222", fg="#999").pack(side="left", padx=(10, 0))

        frame.pack(fill="x", pady=8)
        return e_var

<<<<<<< HEAD
=======
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
>>>>>>> origin/master

    def start(self):
        try:
            s = GameSet(
                bots=int(self.entries['bots'].get()),
<<<<<<< HEAD

                aggro=float(self.entries['aggro'].get()),
                pl_b_max=int(self.entries['pl_b_max'].get()),

                pl_b_pow=int(self.entries['pl_b_pow'].get()),
                tick_ms=int(self.entries['tick_ms'].get())

=======
                aggro=float(self.entries['aggro'].get()),
                pl_b_max=int(self.entries['pl_b_max'].get()),
                pl_b_pow=int(self.entries['pl_b_pow'].get()),
                tick_ms=int(self.entries['tick_ms'].get()),
                pathfinding_algorithm=self.algorithm_var.get(),
                heuristic=self.heuristic_var.get()
>>>>>>> origin/master
            )
            s.aggro = max(0.0, min(1.0, s.aggro))
            
            self.err_lbl.config(text="")
            self.start_cb(s)
<<<<<<< HEAD

=======
>>>>>>> origin/master
        
        except ValueError:
            self.err_lbl.config(text="Invalid input. Please enter valid numbers.")
        except Exception as e:
<<<<<<< HEAD

            self.err_lbl.config(text=f"An error occurred: {e}")
=======
            self.err_lbl.config(text=f"An error occurred: {e}")
>>>>>>> origin/master
