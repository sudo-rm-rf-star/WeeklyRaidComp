from logic.Character import Character
from typing import List
from logic.raid_composition.RaidCompositionEvaluator import RaidCompositionEvaluator

class NaxxRaidCompositionEvaluator(RaidCompositionEvaluator):
    """Evaluates a raid composition. Methods can be overrides for specific raids. """

    def __init__(self, characters: List[Character]):
        super(NaxxRaidCompositionEvaluator, self).__init__("aq", characters)

    def raid_specific_score(self) -> float:
        return 1
