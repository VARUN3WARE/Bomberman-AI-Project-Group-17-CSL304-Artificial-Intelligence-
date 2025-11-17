from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Set
from config import bot_v, bot_aggro

@dataclass
class T:
    typ: int = 0
    b: Optional["B"] = None
    in_expl: bool = False

@dataclass
class Ent:
    x: int
    y: int

    def p(self) -> Tuple[int,int]:
        return (self.x, self.y)

@dataclass
class Bman(Ent):
    i: int
    hp: int
    max_b: int = 1
    b_pow: int = 3
    b_act: int = 0
    live: bool = True
    scr: int = 0

    def can_p(self) -> bool:
        return self.live and self.b_act < self.max_b

@dataclass
class Pl(Bman):
    pass

@dataclass
class Comp(Bman):
    vis: int = bot_v
    aggro: float = bot_aggro
    st: str = "search"
    tgt: Optional[Tuple[int,int]] = None
    pth: List[Tuple[int,int]] = field(default_factory=list)
    last_th: int = field(default=0)
    th_int: int = 400
    pth_tgt: Optional[Tuple[int,int]] = None
    pth_stale: int = 0
    stat: str = "idle"

@dataclass
class B(Ent):
    own: Bman
    expl_at: int
    pow: int = 3
    expl: bool = False

@dataclass
class Expl:
    pos: Set[Tuple[int,int]]
    end: int