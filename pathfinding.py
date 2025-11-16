import heapq
from typing import List, Tuple, Optional, Set, Dict

from utils import manh, neigh
from map import GMap
from config import E


def find_path(g_map:GMap, s:Tuple[int,int], g:Tuple[int,int], forbid:Set[Tuple[int,int]]=set()) -> Optional[List[Tuple[int,int]]]:
    if s == g:

        return []
    oh = []
    heapq.heappush(oh, (manh(s,g), 0, s))

    came: Dict[Tuple[int,int], Tuple[int,int]] = {}
    gs = {s: 0}
    cl = set()

    while oh:
        f,g_cost,curr = heapq.heappop(oh)

        if curr in cl:
            continue

        if curr == g:
            p = []
            c = curr

            while c != s:
                p.append(c)

                c = came[c]
            p.reverse()

            return p
        cl.add(curr)
        x,y = curr
        for nx,ny in neigh(curr):

            if not g_map.in_b(nx,ny): continue
            if (nx,ny) in forbid: continue
            t = g_map.g[ny][nx]
            if t.typ != E: continue

            if t.b is not None: continue
            tent = g_cost + 1
            if (nx,ny) not in gs or tent < gs[(nx,ny)]:

                gs[(nx,ny)] = tent
                came[(nx,ny)] = curr

                heapq.heappush(oh, (tent + manh((nx,ny), g), tent, (nx,ny)))
    return None