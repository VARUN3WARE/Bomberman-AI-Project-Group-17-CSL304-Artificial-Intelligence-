#!/usr/bin/env python3
import tkinter as tk
from src.game import G
from src.ui.settings import SetScreen, GameSet
from src.core.config import WW, WH

class App:
    def __init__(self, r: tk.Tk):
        self.r = r
        self.r.title("Bomberman - Tkinter (AI + Settings)")
        self.r.configure(bg="#111")
        
        self.r.geometry(f"{WW}x{WH + 50}")
        self.r.update_idletasks()
        x = (self.r.winfo_screenwidth() // 2) - (self.r.winfo_width() // 2)
        y = (self.r.winfo_screenheight() // 2) - (self.r.winfo_height() // 2)
        self.r.geometry(f"+{x}+{y}")
        self.r.resizable(False, False)

        self.s = GameSet()
        self.curr_scr = None
        self.show_set_scr()

    def show_set_scr(self):
        if self.curr_scr:
            self.curr_scr.destroy()
        
        self.r.geometry(f"{WW}x{WH + 50}")
        
        self.curr_scr = SetScreen(self.r, self.s, self.start_g)
        self.curr_scr.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.r.unbind("<KeyPress>")
        self.r.unbind("<KeyRelease>")

    def start_g(self, s: GameSet):
        self.s = s
        if self.curr_scr:
            self.curr_scr.destroy()
        
        self.r.geometry(f"{WW}x{WH}")

        self.curr_scr = G(self.r, self.s, self.q)
        self.curr_scr.pack(fill="both", expand=True)
        self.curr_scr.focus_set()

    def q(self):
        if self.curr_scr and isinstance(self.curr_scr, G):
            self.curr_scr.running = False
        self.r.quit()

def m():
    r = tk.Tk()
    app = App(r)
    r.protocol("WM_DELETE_WINDOW", app.q)
    r.mainloop()

if __name__ == "__main__":
    m()
