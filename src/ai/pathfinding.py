import heapq
from typing import List, Tuple, Optional, Set, Dict, Callable

from src.core.utils import manh, neigh, chebyshev, euclidean
from src.game_objects.map import GMap
from src.core.config import E

PathfindingFunc = Callable[[GMap, Tuple[int, int], Tuple[int, int], Set[Tuple[int, int]]], Optional[List[Tuple[int, int]]]]
HeuristicFunc = Callable[[Tuple[int, int], Tuple[int, int]], float]

def a_star_find_path(g_map: GMap, s: Tuple[int, int], g: Tuple[int, int], heuristic: HeuristicFunc, forbid: Set[Tuple[int, int]] = set()) -> Optional[List[Tuple[int, int]]]:
    if s == g:
        return []
    oh = []
    heapq.heappush(oh, (heuristic(s, g), 0, s))

    came: Dict[Tuple[int, int], Tuple[int, int]] = {}
    gs = {s: 0}
    cl = set()

    while oh:
        _, g_cost, curr = heapq.heappop(oh)

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
        for nx, ny in neigh(curr):
            if not g_map.in_b(nx, ny) or (nx, ny) in forbid:
                continue
            
            t = g_map.g[ny][nx]
            if t.typ != E or t.b is not None:
                continue

            tent = g_cost + 1
            if (nx, ny) not in gs or tent < gs[(nx, ny)]:
                gs[(nx, ny)] = tent
                came[(nx, ny)] = curr
                heapq.heappush(oh, (tent + heuristic((nx, ny), g), tent, (nx, ny)))
    return None

def dijkstra_find_path(g_map: GMap, s: Tuple[int, int], g: Tuple[int, int], forbid: Set[Tuple[int, int]] = set()) -> Optional[List[Tuple[int, int]]]:
    return a_star_find_path(g_map, s, g, lambda a, b: 0, forbid)

def bfs_find_path(g_map: GMap, s: Tuple[int, int], g: Tuple[int, int], forbid: Set[Tuple[int, int]] = set()) -> Optional[List[Tuple[int, int]]]:
    if s == g:
        return []
    
    q = [(s, [])]
    visited = {s}

    while q:
        curr, path = q.pop(0)

        if curr == g:
            return path

        for nx, ny in neigh(curr):
            if (nx, ny) not in visited and g_map.in_b(nx, ny) and (nx, ny) not in forbid:
                t = g_map.g[ny][nx]
                if t.typ == E and t.b is None:
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    q.append(((nx, ny), new_path))
    return None

def get_pathfinding_algorithm(name: str) -> PathfindingFunc:
    if name == 'dijkstra':
        return dijkstra_find_path
    elif name == 'bfs':
        return bfs_find_path
    return lambda g_map, s, g, forbid=set(): a_star_find_path(g_map, s, g, manh, forbid)

def get_heuristic(name: str) -> HeuristicFunc:
    if name == 'euclidean':
        return euclidean
    elif name == 'chebyshev':
        return chebyshev
    return manh

def find_path(g_map: GMap, s: Tuple[int, int], g: Tuple[int, int], algorithm: str = 'a_star', heuristic: str = 'manhattan', forbid: Set[Tuple[int, int]] = set()) -> Optional[List[Tuple[int, int]]]:
    path_func = get_pathfinding_algorithm(algorithm)
    
    if algorithm == 'a_star':
        heuristic_func = get_heuristic(heuristic)
        return a_star_find_path(g_map, s, g, heuristic_func, forbid)
    
    return path_func(g_map, s, g, forbid)
