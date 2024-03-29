from logic.Character import Character
from typing import List
from logic.raid_composition.RaidCompositionEvaluator import RaidCompositionEvaluator
from logic.enums.Role import Role
from logic.enums.Class import Class


class AQRaidCompositionEvaluator(RaidCompositionEvaluator):
    """Evaluates a raid composition. Methods can be overrides for specific raids. """

    def __init__(self, characters: List[Character]):
        super(AQRaidCompositionEvaluator, self).__init__("aq", characters)

    def raid_specific_score(self) -> float:
        """ 15 Melees/Hunters/Off-tanks for soaking, 3 Hunters for NR buff """
        is_viable = self.count_character(role=Role.MELEE) >= 15 \
                    and self.count_character(role=Role.TANK) - 1 \
                    and self.count_character(klass=Class.HUNTER) >= 3
        return 1 if is_viable else 0
