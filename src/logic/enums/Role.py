from enum import Enum, auto


class Role(Enum):
    MELEE = auto()
    RANGED = auto()
    TANK = auto()
    HEALER = auto()

    def __lt__(self, other):
        return self.value < other.value
