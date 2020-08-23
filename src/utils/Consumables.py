from logic.enums.Class import Class
from logic.enums.Role import Role
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class ConsumableRequirement:
    # Names for the consumables
    consumable_names: List[str]
    # Indicates whether everyone needs the consumable
    everyone: bool = False
    # All roles which need the consumable
    roles: List[Role] = field(default_factory=list)
    # All classes which need the consumable
    classes: List[Class] = field(default_factory=list)
    # All role, class combination which need the consumable
    role_classes: List[Tuple[Role, Class]] = field(default_factory=list)


def casters() -> List[Tuple[Role, Class]]:
    return [
        (Role.RANGED, Class.MAGE),
        (Role.RANGED, Class.WARLOCK),
        (Role.RANGED, Class.DRUID),
        (Role.RANGED, Class.PRIEST)
    ]


def get_consumable_requirements(raid_name: str) -> List[ConsumableRequirement]:
    return CONSUMABLE_REQUIREMENTS.get(raid_name, []) + CONSUMABLE_REQUIREMENTS['all']


#  https://docs.google.com/spreadsheets/d/1JiwdusZfL_37YFjgHB3wPr0pdDgySBEyY6zRKoXEfgA/edit#gid=0
CONSUMABLE_REQUIREMENTS = {
    'aq': [
        ConsumableRequirement(["Nature Protection"], everyone=True),
    ],
    'all': [
        ConsumableRequirement(["Elixir of the Mongoose", "Greater Agility"], roles=[Role.TANK, Role.MELEE],
                              classes=[Class.HUNTER]),
        ConsumableRequirement(["Health II"], roles=[Role.TANK]),
        ConsumableRequirement(["Greater Arcane Elixir", "Arcane Elixir"], role_classes=casters()),
        ConsumableRequirement(["Brilliant Wizard Oil"], role_classes=casters()),
        ConsumableRequirement(["Greater Firepower", "Fire Power", "Frost Power, Shadow Power"],
                              classes=[Class.MAGE, Class.WARLOCK]),
        ConsumableRequirement(["Brilliant Mana Oil"], roles=[Role.HEALER]),
        ConsumableRequirement(["Mana Regeneration"], roles=[Role.HEALER]),
        ConsumableRequirement(["Healing Potion"], roles=[Role.MELEE, Role.TANK, Role.RANGED]),
        ConsumableRequirement(["Restore Mana"], roles=[Role.HEALER]),
    ]
}
