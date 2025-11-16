import tkinter as tk
import random
from collections import deque
from typing import List, Tuple, Optional, Set, Dict

from utils import now, manh, neigh
from config import *

from settings import GameSet
from entities import Pl, Comp, B, Expl, Bman
from map import GMap

from pathfinding import find_path


class G(tk.Frame):
    def __init__(self, r, s: GameSet, on_q):

        super().__init__(r, bg="#111")
        self.s = s
        self.on_q = on_q

        self.t_ms = self.s.tick_ms
        self.b_think_int = self.t_ms * 5

        self.c = tk.Canvas(self, width=WW, height=WH, bg="#111", highlightthickness=0)

        self.c.pack()
        self.m = GMap(MW, MH, s=0xBEEF)
        self.ps: List[Pl] = []
        self.bs: List[Comp] = []

        self.boms: List[B] = []
        self.expls: List[Expl] = []
        self.n_id = 1
        self.msgs: List[str] = []

        self.l_msg = ""
        self.setup_e()
        self.k_st = set()

        self.bind_k()
        self.run = True
        self.l_tick = now()

        self.g_over = False
        self.g_res = ""
        self.after(self.t_ms, self.tick)

        self.d()


    def setup_e(self):
        p = Pl(x=1, y=1, i=self.gen_id(), hp=p_hp,

                   max_b=self.s.pl_b_max,
                   b_pow=self.s.pl_b_pow)

        self.ps.append(p)


        rng = random.Random()

        tries = 0

        positions = []
        while len(positions) < self.s.bots and tries < 1000:

            tries += 1

            x = rng.randint(1, self.m.w-2)

            y = rng.randint(1, self.m.h-2)

            if (x,y) == (p.x,p.y): continue

            if self.m.g[y][x].typ != E: continue

            if self.is_occ(x,y): continue
            positions.append((x,y))
        

        for pos in positions:

            b = Comp(x=pos[0], y=pos[1], i=self.gen_id(), hp=b_hp,
                         max_b=b_bombs,

                         b_pow=b_power,

                         vis=self.s.vis,

                         aggro=self.s.aggro,
                         th_int=self.b_think_int)

            self.bs.append(b)


    def gen_id(self) -> int:

        nid = self.n_id

        self.n_id += 1

        return nid


    def bind_k(self):

        self.master.bind("<KeyPress>", self.on_k_press)
        self.master.bind("<KeyRelease>", self.on_k_rel)


    def on_k_press(self, e):

        k = e.keysym.lower()

        self.k_st.add(k)

        if k in ("space",):

            self.p_bomb(self.ps[0])
        if k in ("q","escape"):

            self.q()



    def on_k_rel(self, e):

        k = e.keysym.lower()

        if k in self.k_st:

            self.k_st.remove(k)


    def q(self):

        self.run = False
        self.on_q()


    def add_m(self, txt:str):

        self.l_msg = txt

        self.msgs.append(txt)

        if len(self.msgs) > 6:

            self.msgs.pop(0)

    def is_occ(self, x: int, y: int, ign: Optional[Bman] = None) -> bool:
        for p in self.ps:

            if p is ign:
                continue
            if p.live and p.x == x and p.y == y:

                return True

        for b in self.bs:
            if b is ign:

                continue
            if b.live and b.x == x and b.y == y:
                return True
        return False


    def p_bomb(self, own:Bman) -> bool:
        if not own.can_p():
            return False

        x,y = own.x, own.y

        t = self.m.g[y][x]

        if t.b is not None:

            return False
        if isinstance(own, Comp):
            if not self.can_esc(own):
                own.stat = "refused bomb (no escape)"
                return False

        expl_t = now() + fuse

        bom = B(x=x, y=y, own=own, expl_at=expl_t, pow=own.b_pow)
        self.boms.append(bom)

        self.m.set_b(x,y,bom)
        own.b_act += 1

        own.stat = f"placed bomb at {x},{y}"
        self.add_m(f"Bomb placed by {own.i} at {x},{y}")

        if isinstance(own, Comp):
            self.plan_esc(own, bom)
        return True



    def expl_b(self, bom:B):
        if bom.expl: return

        bom.expl = True
        self.m.set_b(bom.x, bom.y, None)
        try:
            self.boms.remove(bom)
        except ValueError:

            pass
        bom.own.b_act = max(0, bom.own.b_act - 1)
        pos: Set[Tuple[int,int]] = {(bom.x, bom.y)}

        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:

            for st in range(1, bom.pow+1):
                nx = bom.x + dx*st
                ny = bom.y + dy*st

                if not self.m.in_b(nx,ny):

                    break
                t = self.m.g[ny][nx]

                if t.typ == H:
                    break

                pos.add((nx,ny))
                if t.b and not t.b.expl:

                    self.expl_b(t.b)

                if t.typ == S:

                    break

        dest = 0

        for (x,y) in list(pos):
            if self.m.del_s(x,y):
                dest += 1
        if dest:

            self.add_m(f"{dest} soft wall(s) destroyed")

        for p in self.ps:

            if p.live and (p.x,p.y) in pos:
                p.hp -= 1
                self.add_m(f"Player hit! HP {p.hp}")

                if p.hp <= 0:

                    p.live = False
                    self.add_m("Player died!")

        for b in self.bs:
            if b.live and (b.x,b.y) in pos:

                b.hp -= 1

                if b.hp <= 0:
                    b.live = False
                    if isinstance(bom.own, Pl):

                        bom.own.scr += 100
                    self.add_m(f"Bot {b.i} killed by bomb")

        exp = Expl(pos=pos, end=now() + expl_ms)

        self.expls.append(exp)


    def pred_d_times(self) -> Dict[Tuple[int,int], int]:

        dang = {}
        n = now()
        for b in self.boms:
            t_left = max(0, b.expl_at - n)

            pos = [(b.x, b.y)]

            for dx,dy in [(1,0),(-1,0),(0,1),(-1,0)]:

                for st in range(1, b.pow+1):

                    nx = b.x + dx*st

                    ny = b.y + dy*st
                    if not self.m.in_b(nx,ny): break
                    if self.m.g[ny][nx].typ == H: break

                    pos.append((nx,ny))

                    if self.m.g[ny][nx].typ == S:

                        break

            for p in pos:
                prev = dang.get(p, None)
                if prev is None or t_left < prev:

                    dang[p] = t_left
        return dang



    def find_s_path(self, bot:Comp, d_times:Dict[Tuple[int,int],int]) -> Optional[List[Tuple[int,int]]]:

        s = (bot.x, bot.y)

        q = deque([(s, 0, [])])

        vis = {s}
        
        s_cands: List[Tuple[List[Tuple[int,int]], Tuple[int,int]]] = []
        MAX_C = 5
        MAX_S = 20

        while q:
            cur, steps, pth = q.popleft()

            if steps > MAX_S:
                continue


            arr_ms = steps * bot.th_int

            dt = d_times.get(cur, None)

            if steps > 0 and ((dt is None) or (dt > arr_ms + safe_m)):

                if self.m.is_w(cur[0], cur[1]):
                    s_cands.append((pth, cur))
                    if len(s_cands) >= MAX_C:

                        break


            for nx,ny in neigh(cur):

                if not self.m.in_b(nx,ny): continue
                if (nx,ny) in vis: continue

                if not self.m.is_w(nx,ny): continue
                

                vis.add((nx,ny))

                new_path = pth + [(nx,ny)]
                q.append(((nx,ny), steps+1, new_path))

        

        if not s_cands:

            return None



        b_path = None

        b_score = -1_000_000
        

        for pth, pos in s_cands:

            scr = self.calc_open(pos)
            

            c_score = (scr * 100) - len(pth)

            
            if c_score > b_score:
                b_score = c_score
                b_path = pth

        return b_path

    def find_n_s(self, bot:Comp) -> Optional[Tuple[int,int]]:
        best = None
        bestd = 10**9
        for y in range(self.m.h):
            for x in range(self.m.w):
                if self.m.g[y][x].typ == S:
                    d = manh((bot.x,bot.y),(x,y))
                    if d < bestd:
                        bestd = d


                        best = (x,y)
        return best

    def can_esc(self, bot:Comp) -> bool:
        bx,by = bot.x, bot.y
        pos = {(bx,by)}
        for dx,dy in [(1,0),(-1,0),(0,1),(-1,0)]:

            for st in range(1, bot.b_pow+1):
                nx = bx + dx*st

                ny = by + dy*st

                if not self.m.in_b(nx,ny): break
                if self.m.g[ny][nx].typ == H: break
                pos.add((nx,ny))
                if self.m.g[ny][nx].typ == S: break
        
        m_steps = max(1, (fuse - safe_m) // bot.th_int)
        q = deque([((bot.x,bot.y), 0)])
        vis = {(bot.x,bot.y)}
        while q:
            (cx,cy), steps = q.popleft()

            

            if steps > 0 and (cx,cy) not in pos and self.m.is_w(cx,cy):
                if steps <= m_steps:

                    return True
            
            if steps >= m_steps: continue
            for nx,ny in neigh((cx,cy)):
                if not self.m.in_b(nx,ny): continue
                if (nx,ny) in vis: continue
                if not self.m.is_w(nx,ny):
                    continue
                vis.add((nx,ny))
                q.append(((nx,ny), steps+1))
        return False

    def plan_esc(self, bot:Comp, bom:B):
        n = now()
        dang = self.pred_d_times()
        m_steps = max(1, (bom.expl_at - n - safe_m) // bot.th_int)
        s = (bot.x, bot.y)
        q = deque([(s, 0, [])])
        vis = {s}


        while q:
            (cx,cy), steps, pth = q.popleft()

            if steps <= m_steps and self.m.is_w(cx,cy):

                dt = dang.get((cx,cy), None)
                arr_ms = steps * bot.th_int

                if steps > 0 and ((dt is None) or (dt > arr_ms + safe_m)):

                    bot.pth = pth

                    bot.pth_tgt = (cx,cy)

                    bot.pth_stale = n + repath_hold
                    bot.stat = f"escaping to {cx,cy} after bomb"

                    return


            if steps >= m_steps: continue
            for nx,ny in neigh((cx,cy)):

                if not self.m.in_b(nx,ny): continue
                if (nx,ny) in vis: continue

                if not self.m.is_w(nx,ny): continue

                vis.add((nx,ny))

                new_path = pth + [(nx,ny)]
                q.append(((nx,ny), steps+1, new_path))
        
        bot.stat = "placed bomb but no escape found"


    def calc_open(self, pos: Tuple[int, int]) -> int:

        scr = 0
        for nx, ny in neigh(pos):

            if self.m.is_w(nx, ny):
                scr += 1
        return scr

    def upd_ai(self):
        n = now()
        pl = self.ps[0]
        d_times = self.pred_d_times()
        for bot in self.bs:
            if not bot.live:
                bot.stat = "dead"
                continue
            if n - bot.last_th < bot.th_int:
                self.follow_pth(bot, d_times)
                continue
            bot.last_th = n
            if (bot.x,bot.y) in d_times and d_times[(bot.x,bot.y)] <= bot.th_int + safe_m:
                bot.st = "evade"
            else:
                if manh((bot.x,bot.y),(pl.x,pl.y)) <= bot.vis:
                    bot.st = "chase"
                    bot.tgt = (pl.x, pl.y)
                else:


                    bot.st = "search"
                    bot.tgt = None
            

            if bot.st == "evade":

                pth = self.find_s_path(bot, d_times)
                if pth:

                    dest = pth[-1] if pth else (bot.x, bot.y)

                    bot.pth = pth

                    bot.pth_tgt = dest
                    bot.pth_stale = n + repath_hold
                    bot.stat = f"evading -> {dest} (path {len(pth)})"

                    self.follow_pth(bot, d_times)

                else:

                    bot.stat = "evade: no path, random move"
                    self.rand_mov(bot, d_times)

            

            elif bot.st == "chase":
                if not bot.pth:
                    pth = find_path(self.m, (bot.x,bot.y), (pl.x,pl.y))

                    if pth and len(pth) > 0:
                        bot.pth = pth

                        bot.pth_tgt = (pl.x,pl.y)
                        bot.pth_stale = n + repath_hold
                        bot.stat = f"chase: new path -> {pl.x,pl.y}"

                    else:

                        bot.stat = "chase: no path, roam"

                        self.rand_mov(bot, d_times)
                        continue 

                else:
                    bot.stat = f"chase: following path to {bot.pth_tgt}"


                if manh((bot.x,bot.y),(pl.x,pl.y)) <= 2 and bot.can_p():
                    if random.random() < bot.aggro and self.can_esc(bot):

                        bot.stat = f"chase: placing bomb (aggro {bot.aggro})"
                        self.p_bomb(bot) 

                    else:
                        bot.stat = "chase: close but refused bomb or not placing"
                

                self.follow_pth(bot, d_times)
            

            else:
                current_target_valid = False
                if bot.pth_tgt:

                    tx, ty = bot.pth_tgt

                    if self.m.in_b(tx, ty) and self.m.g[ty][tx].typ == S:
                         current_target_valid = True


                if not bot.pth or not current_target_valid:
                    tgt = self.find_n_s(bot)

                    if tgt:
                        pth = find_path(self.m, (bot.x,bot.y), tgt)
                        if pth:

                            bot.pth = pth

                            bot.pth_tgt = tgt
                            bot.pth_stale = n + repath_hold

                            
                            if len(pth) <= 1 and bot.can_p() and random.random() < (bot.aggro / 2):
                                if self.can_esc(bot):

                                    bot.stat = f"search: breaking wall at {tgt}"

                                    self.p_bomb(bot)

                                else:
                                    bot.stat = "search: wanted to bomb but unsafe"

                            else:

                                bot.stat = f"search -> soft at {tgt} (path {len(pth)})"

                            self.follow_pth(bot, d_times)

                            continue

                
                bot.stat = "search: roam"
                self.rand_mov(bot, d_times)


    def follow_pth(self, bot:Comp, d_times:Dict[Tuple[int,int],int]={}):
        if not bot.pth:

            n = now()
            if bot.pth_tgt and n < bot.pth_stale:
                if bot.st != "chase":
                    pth = find_path(self.m, (bot.x,bot.y), bot.pth_tgt)
                    if pth:
                        bot.pth = pth
                        bot.stat = f"replan -> {bot.pth_tgt} (path {len(pth)})"
            return
        


        nx, ny = bot.pth[0]
        arr_ms = bot.th_int
        dt = d_times.get((nx,ny), None)

        if dt is not None and dt <= arr_ms + safe_m:
            bot.pth = []

            bot.pth_stale = now() + repath_hold

            bot.stat = f"avoiding dangerous step {nx,ny}"

            return
        

        if self.m.is_w(nx, ny) and not self.is_occ(nx, ny, ign=bot):
            bot.x, bot.y = nx, ny
            bot.pth.pop(0)

            if bot.pth:
                bot.stat = f"moved -> {bot.x,bot.y} (remaining {len(bot.pth)})"

            else:

                bot.stat = f"arrived at {bot.x, bot.y}"
        else:
            bot.pth = []
            bot.pth_stale = now() + repath_hold

            bot.stat = "blocked, will replan"


    def rand_mov(self, bot:Comp, d_times:Dict[Tuple[int,int],int]={}):
        dirs = [(1,0),(-1,0),(0,1),(-1,0)]
        random.shuffle(dirs)

        for dx,dy in dirs:

            nx,ny = bot.x + dx, bot.y + dy

            if (self.m.in_b(nx,ny)
                and self.m.is_w(nx,ny)

                and not self.is_occ(nx,ny, ign=bot)):

                arr_ms = bot.th_int
                dt = d_times.get((nx,ny), None)

                if dt is not None and dt <= arr_ms + safe_m:

                    continue

                bot.x, bot.y = nx, ny

                bot.stat = f"random moved -> {bot.x,bot.y}"
                return

        bot.stat = "random: no move"


    def tick(self):

        if not self.run:

            return

        n = now()

        
        for y in range(self.m.h):

            for x in range(self.m.w):

                self.m.g[y][x].in_expl = False

        for exp in self.expls:

            if exp.end > n:

                for (ex,ey) in exp.pos:

                    if self.m.in_b(ex,ey):

                        self.m.g[ey][ex].in_expl = True

        

        self.h_input()
        self.upd_ai()
        
        n = now()
        for b in list(self.boms):
            if n >= b.expl_at and not b.expl:
                self.expl_b(b)
        
        self.expls = [e for e in self.expls if e.end > n]

        if not self.g_over:
            if not self.ps[0].live:
                self.g_over = True
                self.g_res = "lose"
            elif all(not b.live for b in self.bs):
                self.g_over = True
                self.g_res = "win"

        
        for y in range(self.m.h):
            for x in range(self.m.w):
                self.m.g[y][x].in_expl = False
        for exp in self.expls:
            if exp.end > n:
                for (ex,ey) in exp.pos:

                    if self.m.in_b(ex,ey):

                        self.m.g[ey][ex].in_expl = True

        
        self.d()

        self.after(self.t_ms, self.tick)


    def h_input(self):

        p = self.ps[0]

        if not p.live: return

        dx = dy = 0
        if any(k in self.k_st for k in ("up","w")):

            dy = -1

        elif any(k in self.k_st for k in ("down","s")):

            dy = 1

        elif any(k in self.k_st for k in ("left","a")):
            dx = -1

        elif any(k in self.k_st for k in ("right","d")):

            dx = 1

        if dx != 0 or dy != 0:

            nx,ny = p.x + dx, p.y + dy

            if (self.m.in_b(nx,ny)

                and self.m.is_w(nx,ny)
                and not self.is_occ(nx,ny)):

                p.x, p.y = nx, ny


    def d(self):
        self.c.delete("all")
        for y in range(self.m.h):
            for x in range(self.m.w):
                l = x*C
                t = y*C
                tile = self.m.g[y][x]
                if tile.in_expl:
                    col = "#ffb26b"
                elif tile.typ == H:
                    col = "#444444"
                elif tile.typ == S:
                    col = "#a0522d"
                else:
                    col = "#202020"
                self.c.create_rectangle(l, t, l+C, t+C, fill=col, outline="#111")
                if tile.b is not None:

                    b = tile.b

                    rem = max(0, b.expl_at - now())

                    sc = 0.45 + 0.5 * (rem / fuse)

                    pad = int((1-sc) * C / 2)
                    self.c.create_oval(l+pad, t+pad, l+C-pad, t+C-pad, fill="#ffdd55", outline="#ccaa22")

        for exp in self.expls:

            for (ex,ey) in exp.pos:

                l = ex*C; t = ey*C
                self.c.create_rectangle(l, t, l+C, t+C, fill="#ff8c42", outline="#f97306")
        for b in self.bs:
            if not b.live: continue
            l = b.x*C; t = b.y*C
            mar = 6
            self.c.create_rectangle(l+mar, t+mar, l+C-mar, t+C-mar, fill="#d54", outline="#900")
        p = self.ps[0]
        l = p.x*C; t = p.y*C
        mar = 6
        col = "#4f4" if p.live else "#666"
        self.c.create_rectangle(l+mar, t+mar, l+C-mar, t+C-mar, fill=col, outline="#060")
        hud_y = self.m.h * C + 8

        hud_txt = f"HP: {p.hp}  Score: {p.scr}  Bombs: {p.b_act}/{p.max_b}  Time: {int((now()/1000))}s"

        self.c.create_text(8, hud_y, anchor="w", fill="#eee", font=("Consolas", 13), text=hud_txt)

        if self.msgs:
            for i, m in enumerate(reversed(self.msgs[-6:])):

                self.c.create_text(8, hud_y + 22 + i*16, anchor="w", fill="#ddd", font=("Consolas", 11), text=m)
        for i, b in enumerate(self.bs):
            st_txt = f"Bot {b.i}: {b.stat}  state={b.st} target={b.tgt} path_len={len(b.pth)}"

            self.c.create_text(WW - 8, hud_y + 6 + i*16, anchor="e", fill="#ffd", font=("Consolas", 12), text=st_txt)


        if self.g_over:

            self.c.create_rectangle(0, 0, WW, WH, fill="#000", stipple="gray50")

            msg = "You Win!" if self.g_res == "win" else "You Lose!"

            self.c.create_text(WW/2, WH/2 - 40, text=msg, font=("Consolas", 48, "bold"), fill="#fff")

            self.c.create_text(WW/2, WH/2 + 20, text="Press Q to Exit", font=("Consolas", 20), fill="#fff")
