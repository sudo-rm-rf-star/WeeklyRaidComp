from enum import Enum, auto
from logic.enums.Role import Role
from typing import List


class Class(Enum):
    WARLOCK = [("Affliction", Role.RANGED), ("Demonology", Role.RANGED), ("Destruction", Role.RANGED)]
    PRIEST = [("Discipline", Role.HEALER), ("Holy", Role.HEALER), ("Shadow", Role.RANGED)]
    MAGE = [("Arcane", Role.RANGED), ("Fire", Role.RANGED), ("Frost", Role.RANGED)]
    ROGUE = [("Assassination", Role.MELEE), ("Combat", Role.MELEE), ("Subtlety", Role.MELEE)]
    DRUID = [("Balance", Role.RANGED), ("Feral", Role.MELEE), ("Bear", Role.TANK), ("Restoration", Role.HEALER)]
    HUNTER = ["Beast Mastery", ("Marksmanship", Role.RANGED), ("Survival", Role.RANGED)]
    PALADIN = [("Holy", Role.HEALER), ("Protection", Role.TANK), ("Retribution", Role.MELEE)]
    WARRIOR = [("Arms", Role.MELEE), ("Fury", Role.MELEE), ("Protection", Role.TANK)]
    SHAMAN = [("Elemental", Role.RANGED), ("Enhancement", Role.MELEE), ("Restoration", Role.HEALER)]

    def __init__(self, specs: List[str]):
        self.specs = specs

    def get_role(self, spec: str):
        return {x: y for x, y in self.specs}[spec]

    def __lt__(self, other):
        return self.value < other.value
