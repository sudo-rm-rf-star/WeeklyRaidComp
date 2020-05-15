from utils.Constants import pref_per_role, min_per_class_role, max_per_class_role
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from logic.Player import Player
from pandas import DataFrame
from logic.enums.Role import Role
from typing import List, Dict, Tuple
import utils.Logger as Log


def make_raid_composition(raid_name: str, players: List[Player]) -> List[Player]:
    """
    Updates roster status of all players and returns a list of updated players
    """
    if len(players) == 0:
        Log.error("No players found. Returning.")
        return []

    players_by_name = {player.name: player for player in players}
    players_df = players_dataframe(raid_name, players)
    updated_players = []

    def eligible() -> DataFrame:
        return players_df[(players_df['signee_choice'] != SignupStatus.DECLINE) & (players_df['roster_status'] != RosterStatus.DECLINE)]

    for role, signees_for_role in eligible().groupby('role'):
        for clazz, signees_for_class in signees_for_role.groupby("class"):
            for i, (j, signee) in enumerate(
                    signees_for_class.sort_values('standby_count', ascending=False).iterrows()):
                score = _calculate_importance(i, min_per_class_role[raid_name][role][clazz],
                                              max_per_class_role[raid_name][role][clazz])
                players_df.at[j, "score"] = score

    for role, signees_for_role in eligible().sort_values(['priority', 'score'], ascending=False).groupby('role'):
        pref_count = pref_per_role[raid_name][role]
        accepted_for_role = signees_for_role.iloc[:pref_count]
        not_accepted_for_role = signees_for_role.iloc[pref_count:]

        for _, player in accepted_for_role.iterrows():
            set_roster_choice(updated_players, players_by_name[player['name']], RosterStatus.ACCEPT)

        for _, player in not_accepted_for_role.iterrows():
            set_roster_choice(updated_players, players_by_name[player['name']], RosterStatus.EXTRA)

    for _, player in players_df[players_df['signee_choice'] == SignupStatus.DECLINE].iterrows():
        set_roster_choice(updated_players, players_by_name[player['name']], RosterStatus.DECLINE)

    return updated_players


def players_dataframe(raid_name: str, players: List[Player]) -> DataFrame:
    raid_players = []
    for player in players:
        role = get_role(player.role)
        klass = player.klass.name.lower()
        signee_choice = player.signup_status
        roster_choice = player.roster_status
        priority = signee_choice.value + roster_choice.value
        standby_count = player.get_standby_count(raid_name)
        raid_players.append({'name': player.name, 'class': klass, 'role': role, 'standby_count': standby_count,
                             'signee_choice': signee_choice, 'roster_status': roster_choice, 'priority': priority, 'score': 0})
    return DataFrame(raid_players)


def actual_vs_expected_per_role(raid_name: str, players: List[Player]) -> Dict[str, Tuple[int, int]]:
    actual_vs_expected = {
        'tank': [0, pref_per_role[raid_name]['tank']],
        'healer': [0, pref_per_role[raid_name]['healer']],
        'dps': [0, pref_per_role[raid_name]['dps']]
    }

    for player in players:
        roster_choice = player.roster_status
        if roster_choice == RosterStatus.ACCEPT:
            role = get_role(player.role)
            actual_vs_expected[role][0] += 1

    return {role: tuple(counts) for role, counts in actual_vs_expected.items()}


def set_roster_choice(players: List[Player], player: Player, roster_choice: RosterStatus):
    if player.roster_status != roster_choice:
        player.roster_status = roster_choice
        players.append(player)


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
