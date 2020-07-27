from logic.Character import Character
from logic.enums.Class import Class
from logic.enums.Role import Role
from logic.enums.Race import Race
from typing import Set
import math
from datetime import datetime
from typing import Set
from logic.raid_composition.RaidCompositionEvaluator import RaidCompositionEvaluator
from logic.enums.Role import Role
from logic.enums.Class import Class
from logic.enums.Race import Race


class BWLRaidCompositionEvaluator(RaidCompositionEvaluator):
    """Evaluates a raid composition. Methods can be overrides for specific raids. """

    def __init__(self, characters: Set[Character]):
        super(BWLRaidCompositionEvaluator, self).__init__("bwl", characters)

    def raid_specific_score(self) -> float:
        """ 3 Hunters for tranq rotation, 1 Dwarf Priest for Fear Ward """
        is_viable = self.count_character(klass=Class.HUNTER) >= 3 \
                    and self.contains_character(klass=Class.PRIEST, race=Race.DWARF)
        return 1 if is_viable else 0
