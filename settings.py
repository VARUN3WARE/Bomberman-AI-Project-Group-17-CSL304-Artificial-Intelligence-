import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
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

class SetScreen(tk.Frame):
    def __init__(self, root, init_set: GameSet, start_cb):
        super().__init__(root, bg="#222", padx=20, pady=20)
        self.start_cb = start_cb
        



        tk.Label(self, text="Bomberman Settings", font=("Consolas", 24, "bold"), bg="#222", fg="#eee").pack(pady=(0, 25))

        self.entries = {}
        
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


        self.err_lbl = tk.Label(self, text="", font=("Consolas", 12), bg="#222", fg="#ff5555")
        self.err_lbl.pack(pady=(10, 0))


        tk.Button(self, text="Start Game", command=self.start,
                  font=("Consolas", 16, "bold"), bg="#4f4", fg="#111",
                  relief="flat", pady=10).pack(pady=(20, 0), fill="x")


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


    def start(self):
        try:
            s = GameSet(
                bots=int(self.entries['bots'].get()),

                aggro=float(self.entries['aggro'].get()),
                pl_b_max=int(self.entries['pl_b_max'].get()),

                pl_b_pow=int(self.entries['pl_b_pow'].get()),
                tick_ms=int(self.entries['tick_ms'].get())

            )
            s.aggro = max(0.0, min(1.0, s.aggro))
            
            self.err_lbl.config(text="")
            self.start_cb(s)

        
        except ValueError:
            self.err_lbl.config(text="Invalid input. Please enter valid numbers.")
        except Exception as e:

            self.err_lbl.config(text=f"An error occurred: {e}")