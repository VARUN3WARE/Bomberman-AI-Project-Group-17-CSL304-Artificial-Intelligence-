import time
from typing import Tuple, List
import math

def now() -> int:
    return int(time.time() * 1000)

def manh(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def chebyshev(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def euclidean(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def neigh(p: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = p
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
