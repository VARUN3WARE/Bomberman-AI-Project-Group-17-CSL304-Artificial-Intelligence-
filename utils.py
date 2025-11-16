import time
from typing import Tuple

def now() -> int:
    return int(time.time() * 1000)

def manh(a:Tuple[int,int], b:Tuple[int,int]) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def neigh(pos:Tuple[int,int]):
    x,y = pos
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]