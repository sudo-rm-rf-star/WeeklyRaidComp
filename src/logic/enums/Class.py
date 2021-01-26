from enum import Enum, auto


class Class(Enum):
    WARLOCK = auto()
    PRIEST = auto()
    MAGE = auto()
    ROGUE = auto()
    DRUID = auto()
    HUNTER = auto()
    PALADIN = auto()
    WARRIOR = auto()

    def __lt__(self, other):
        return self.value < other.value
