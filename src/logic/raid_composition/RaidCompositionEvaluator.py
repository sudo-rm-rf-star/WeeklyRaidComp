from logic.Character import Character
from logic.enums.Class import Class
from logic.enums.Role import Role
from logic.enums.Race import Race
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from typing import List
import math
from datetime import datetime
from utils.DateOptionalTime import DateOptionalTime

"""
# Goal
Compute f(X) -> y where X is a set of character instances, f evaluates X resulting in a score Y.

Our scoring function f computes a value that rates how good a composition is based on sets of rules:

# General rules
Rules which apply to all raids

# Raid specific rules
Rules which only apply to specific raids
"""


class RaidCompositionEvaluator:
    """Evaluates a raid composition. Methods can be overrides for specific raids. """

    def __init__(self, raid_name: str, characters: List[Character]):
        self.characters = characters
        self.raid_name = raid_name
        self.characters_per_class = {klass: 0 for klass in Class}
        for character in self.characters:
            self.characters_per_class[character.klass] += 1

    def score(self) -> float:
        score_eval_functions_and_weights = [(self.buff_score, 1), (self.role_score, 2), (self.class_balance_score, 1),
                                            (self.raid_specific_score, 1), (self.standby_score, 1),
                                            (self.signup_status_score, 1)]

        for eval_score, weight in score_eval_functions_and_weights:
            print(eval_score, eval_score(), weight)
        return sum(eval_score() for eval_score, _ in score_eval_functions_and_weights) / sum(
            [weight for _, weight in score_eval_functions_and_weights])

    def buff_score(self) -> float:
        """ Maximize (de)buffs. """
        buff_count = 0
        total_buffs = 0

        attack_power_group_count = int(
            math.ceil((self.count_character(role=Role.MELEE) + self.count_character(role=Role.TANK)) / 5))
        spell_power_group_count = int(
            math.ceil((self.count_character(role=Role.RANGED) - self.count_character(klass=Class.HUNTER)) / 5))

        # Warrior
        if self.contains_character(klass=Class.WARRIOR):
            buff_count += 1  # Sunder Armor
        buff_count += min(self.count_character(klass=Class.WARRIOR), attack_power_group_count)  # Battle Shout per group
        total_buffs += 1 + attack_power_group_count

        # Mage
        if self.contains_character(klass=Class.MAGE):
            buff_count += 1  # Arcane Brilliance
        total_buffs += 1

        # Priest
        if self.contains_character(klass=Class.PRIEST):
            buff_count += 2  # Prayer of Fortitude / Divine Spirit
        total_buffs += 2

        # Shadow Priest
        if self.contains_character(klass=Class.PRIEST, role=Role.RANGED):
            buff_count += 1  # Shadow Weaving
        total_buffs += 1

        # Hunter
        buff_count += min(self.count_character(klass=Class.HUNTER), attack_power_group_count)  # Trueshot Aura
        total_buffs += attack_power_group_count

        # Warlock
        if self.contains_character(klass=Class.WARLOCK):
            # Bloodpact / Soulstone / Healthstone / Curse of Recklessness, Shadow, Elements
            buff_count += 3 + min(self.count_character(klass=Class.WARLOCK), 3)
        total_buffs += 6

        # Druid
        if self.contains_character(klass=Class.DRUID):
            # Mark of the Wild / Thorns / Faerie Fire
            buff_count += 3
        total_buffs += 3

        leader_of_the_pack_count = self.count_character(klass=Class.DRUID, role=Role.MELEE) + self.count_character(
            klass=Class.DRUID, role=Role.TANK)
        buff_count += min(leader_of_the_pack_count, attack_power_group_count)
        total_buffs += attack_power_group_count  # Leader of the Pack

        moonkin_count = self.count_character(klass=Class.DRUID, role=Role.RANGED)
        buff_count += min(moonkin_count, spell_power_group_count)
        total_buffs += spell_power_group_count  # Moonkin Aura

        # Paladin: Blessing of Might, Salavation, Wisdom, Kings, Light, Sanctuary & Devotion, Concentration, Retribution, Resistance Aura
        buff_count += min(self.count_character(klass=Class.PALADIN) * 2, 10)
        total_buffs += 10

        return buff_count / total_buffs

    def standby_score(self) -> float:
        """ Higher score for recent standby so these people are now in the raid comp """
        # st_score = 1
        # now = DateOptionalTime.now()
        # print(self.characters)
        # for character in self.characters:
        #     for standby_datetime in character.standby_dates.get(self.raid_name, {}):
        #         if standby_datetime < now:
        #             weeks_since_standby = (now.to_datetime() - standby_datetime.to_datetime()).days // 7
        #             st_score -= 1 / (40 * (weeks_since_standby + 1))
        # return max(0, st_score)
        return 0

    def role_score(self) -> float:
        """ Ensure minimal role counts """
        tank_score = min(self.count_character(role=Role.TANK) / 4, 1)
        healer_score = min(self.count_character(role=Role.HEALER) / 12, 1)
        return (tank_score + healer_score) / 2

    def class_balance_score(self) -> float:
        """ Optimize class representation. Shamelessly copied from https://www.youtube.com/watch?v=vqeYmtkhhVE """
        optimal_representation = {
            Class.WARRIOR: (8, 12),
            Class.ROGUE: (4, 6),
            Class.HUNTER: (2, 3),
            Class.MAGE: (5, 8),
            Class.WARLOCK: (4, 6),
            Class.PALADIN: (4, 6),
            Class.PRIEST: (3, 5),
            Class.DRUID: (1, 3)
        }
        class_amount = len(optimal_representation)
        total_score = 0
        for klass, (min_class, max_class) in optimal_representation.items():
            class_count = self.count_character(klass=klass)
            if class_count < min_class:
                cb_score = (min_class - class_count) / min_class
            elif class_count > max_class:
                cb_score = (class_count - max_class) / max_class
            else:
                cb_score = 1
            total_score += cb_score / class_amount
        return total_score

    def signup_status_score(self) -> float:
        score_per_status = {
            SignupStatus.ACCEPT: 1,
            SignupStatus.UNDECIDED: 1,
            SignupStatus.LATE: 0.75,
            SignupStatus.TENTATIVE: 0.5,
            SignupStatus.BENCH: 0.25,
            SignupStatus.DECLINE: 0
        }
        total_score = 0
        for status, score in score_per_status.items():
            total_score += score ** sum([1 for char in self.characters if char.signup_status == status])

        return total_score / len(score_per_status.keys())

    def roster_status_score(self) -> float:
        total_score = 0
        score_per_status = {
            RosterStatus.ACCEPT: 1,
            RosterStatus.EXTRA: 0.75,
            RosterStatus.DECLINE: 0,
            RosterStatus.UNDECIDED: 0.5
        }
        for status, score in score_per_status.items():
            total_score += score ** sum([1 for char in self.characters if char.roster_status == status])

        return total_score / len(score_per_status.keys())

    def raid_specific_score(self) -> float:
        """ Score specific to a given raid """
        return 1

    def contains_character(self, role: Role = None, klass: Class = None, race: Race = None) -> bool:
        return self.count_character(role=role, klass=klass, race=race) > 0

    def count_character(self, role: Role = None, klass: Class = None, race: Race = None) -> int:
        if klass is not None and role is None and race is None:
            return self.characters_per_class[klass]
        return len(self.filter_characters(role=role, klass=klass, race=race))

    def filter_characters(self, role: Role = None, klass: Class = None, race: Race = None) -> List[Character]:
        return [char for char in self.characters
                if (role is None or char.role == role)
                and (klass is None or char.klass == klass)
                and (race is None or char.race == race)]
