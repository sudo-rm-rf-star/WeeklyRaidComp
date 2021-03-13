from logic.Character import Character
from logic.raid_composition.RaidCompositionEvaluator import RaidCompositionEvaluator
from typing import List


class BWLRaidCompositionEvaluator(RaidCompositionEvaluator):
    """Evaluates a raid composition. Methods can be overrides for specific raids. """

    def __init__(self, characters: List[Character]):
        super(BWLRaidCompositionEvaluator, self).__init__("bwl", characters)
