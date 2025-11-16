import random
from typing import List, Optional
from entities import T, B
from config import E, S, H

class GMap:
    def __init__(self, w:int, h:int, s:Optional[int]=None):
        self.w = w

        self.h = h
        self.g: List[List[T]] = [[T() for _ in range(w)] for _ in range(h)]

        self.gen(s)

    def gen(self, s:Optional[int]):

        r = random.Random(s)
        for x in range(self.w):
            self.g[0][x].typ = H

            self.g[self.h-1][x].typ = H
        for y in range(self.h):

            self.g[y][0].typ = H
            self.g[y][self.w-1].typ = H

        for y in range(2, self.h-2):
            for x in range(2, self.w-2):
                if x % 2 == 0 and y % 2 == 0:

                    self.g[y][x].typ = H
        for y in range(1, self.h-1):

            for x in range(1, self.w-1):
                if self.g[y][x].typ != E:
                    continue

                if (x <= 2 and y <= 2) or (x >= self.w-3 and y >= self.h-3):
                    continue
                if r.random() < 0.52:

                    self.g[y][x].typ = S

    def in_b(self, x:int, y:int) -> bool:

        return 0 <= x < self.w and 0 <= y < self.h

    def is_w(self, x:int, y:int) -> bool:

        if not self.in_b(x,y): return False
        t = self.g[y][x]

        if t.typ in (S, H): return False
        if t.b is not None:

            return False
        return True


    def set_b(self, x:int, y:int, b:Optional[B]):
        self.g[y][x].b = b


    def del_s(self, x:int, y:int) -> bool:

        if not self.in_b(x,y): return False
        if self.g[y][x].typ == S:

            self.g[y][x].typ = E
            return True

        return False