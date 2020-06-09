from utils.Constants import default_num_per_raid_role, default_min_per_raid_role_class, default_max_per_raid_role_class
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from logic.Character import Character
from pandas import DataFrame
from logic.enums.Role import Role
from typing import List, Dict, Tuple
import utils.Logger as Log


def make_raid_composition(raid_name: str, characters: List[Character]) -> List[Character]:
    """
    Updates roster status of all characters and returns a list of updated characters
    """
    if len(characters) == 0:
        Log.error("No characters found. Returning.")
        return []

    characters_by_name = {character.name: character for character in characters}
    characters_df = characters_dataframe(raid_name, characters)
    updated_characters = []

    def eligible() -> DataFrame:
        return characters_df[(characters_df['signee_choice'] != SignupStatus.DECLINE) & (characters_df['roster_status'] != RosterStatus.DECLINE)]

    for role, signees_for_role in eligible().groupby('role'):
        for clazz, signees_for_class in signees_for_role.groupby("class"):
            for i, (j, signee) in enumerate(
                    signees_for_class.sort_values('standby_count', ascending=False).iterrows()):
                score = _calculate_importance(i, default_min_per_raid_role_class[raid_name][role][clazz],
                                              default_max_per_raid_role_class[raid_name][role][clazz])
                characters_df.at[j, "score"] = score

    for role, signees_for_role in eligible().sort_values(['priority', 'score'], ascending=False).groupby('role'):
        pref_count = default_num_per_raid_role[raid_name][role]
        accepted_for_role = signees_for_role.iloc[:pref_count]
        not_accepted_for_role = signees_for_role.iloc[pref_count:]

        for _, char in accepted_for_role.iterrows():
            set_roster_choice(updated_characters, characters_by_name[char['name']], RosterStatus.ACCEPT)

        for _, char in not_accepted_for_role.iterrows():
            set_roster_choice(updated_characters, characters_by_name[char['name']], RosterStatus.EXTRA)

    for _, char in characters_df[characters_df['signee_choice'] == SignupStatus.DECLINE].iterrows():
        set_roster_choice(updated_characters, characters_by_name[char['name']], RosterStatus.DECLINE)

    return updated_characters


def characters_dataframe(raid_name: str, characters: List[Character]) -> DataFrame:
    raid_chars = []
    for char in characters:
        role = get_role(char.role)
        klass = char.klass.name.lower()
        signee_choice = char.signup_status
        roster_choice = char.roster_status
        priority = signee_choice.value + roster_choice.value
        standby_count = char.standby_count[raid_name]
        raid_chars.append(
            {'name': char.name, 'class': klass, 'role': role, 'standby_count': standby_count, 'signee_choice': signee_choice, 'roster_status': roster_choice,
             'priority': priority, 'score': 0})
    return DataFrame(raid_chars)


def actual_vs_expected_per_role(raid_name: str, characters: List[Character]) -> Dict[str, Tuple[int, int]]:
    actual_vs_expected = {
        'tank': [0, default_num_per_raid_role[raid_name]['tank']],
        'healer': [0, default_num_per_raid_role[raid_name]['healer']],
        'dps': [0, default_num_per_raid_role[raid_name]['dps']]
    }

    for char in characters:
        roster_choice = char.roster_status
        if roster_choice == RosterStatus.ACCEPT:
            role = get_role(char.role)
            actual_vs_expected[role][0] += 1

    return {role: tuple(counts) for role, counts in actual_vs_expected.items()}


def set_roster_choice(characters: List[Character], char: Character, roster_choice: RosterStatus):
    if char.roster_status != roster_choice:
        char.roster_status = roster_choice
        characters.append(char)


def _calculate_importance(cur: int, mini: int, maxi: int) -> float:
    maxi = max(maxi, cur)
    mini = min(mini - 1, cur)
    cur = max(mini, cur)
    return 1 - (cur - mini) / (maxi - mini)


def get_role(role: Role) -> str:
    return {
        Role.TANK: 'tank',
        Role.MELEE: 'dps',
        Role.RANGED: 'dps',
        Role.HEALER: 'healer'
    }[role]
