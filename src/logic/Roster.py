from collections import defaultdict
from src.common.Constants import pref_per_role, min_per_class_role, max_per_class_role
from src.logic.enums.SignupStatus import SignupStatus
from src.logic.enums.RosterStatus import RosterStatus
from src.logic.Players import Players
from src.exceptions.InternalBotException import InternalBotException
from pandas import DataFrame
from src.logic.enums.Role import Role
from typing import Dict, List


class Roster:
    def __init__(self, roster_choices: Dict[str, RosterStatus] = None):
        self.roster_choices = {} if not roster_choices else roster_choices
        self.updates_since_last_check = []  # List of all updates since last check
        self._missing = None
        self._extra = None

    def update(self, raid_name: str, signee_choices: Dict[str, SignupStatus]):
        """
        Updates the roster with the given signees. Updates all of the updated roster statuses.
        """
        if len(signee_choices.keys()) == 0:
            return False
        players_df = self._get_raid_players_df(raid_name, signee_choices)

        def eligible() -> DataFrame:
            return players_df[players_df['signee_choice'] != SignupStatus.DECLINE]

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
                self.set_roster_choice(player['name'], RosterStatus.ACCEPT)

            for _, player in not_accepted_for_role.iterrows():
                self.set_roster_choice(player['name'], RosterStatus.EXTRA)

        for _, player in players_df[players_df['signee_choice'] == SignupStatus.DECLINE].iterrows():
            self.set_roster_choice(player['name'], RosterStatus.DECLINE)

        return True

    def _get_raid_players_df(self, raid_name: str, signee_choices: Dict[str, SignupStatus]) -> DataFrame:
        raid_players = []
        for player_name, roster_choice in self.roster_choices.items():
            player = Players().get(player_name)
            if not player:
                raise InternalBotException(f"Could not find a registered player named {player_name}")
            role = get_role(player.role)
            klass = player.klass.name.lower()
            signee_choice = signee_choices[player_name]
            standby_count = player.get_standby_count(raid_name)
            priority = signee_choice.value + roster_choice.value
            raid_players.append({'name': player.name, 'class': klass, 'role': role, 'standby_count': standby_count,
                                 'signee_choice': signee_choice, 'roster_status': roster_choice, 'priority': priority, 'score': 0})
        return DataFrame(raid_players)

    def get_players_per_role(self, filter_roster_choice: RosterStatus = None) -> Dict[Role, List[str]]:
        players_per_role = defaultdict(list)
        for player_name, roster_choice in self.roster_choices.items():
            if not filter_roster_choice or roster_choice == filter_roster_choice:
                player = Players().get(player_name)
                players_per_role[player.role].append(player_name)
        return players_per_role

    def missing(self, raid_name):
        missing_per_role = {
            'tank': pref_per_role[raid_name]['tank'],
            'healer': pref_per_role[raid_name]['healer'],
            'dps': pref_per_role[raid_name]['dps']
        }

        for player_name, roster_choice in self.roster_choices.items():
            if roster_choice == RosterStatus.ACCEPT:
                player = Players().get(player_name)
                role = get_role(player.role)
                missing_per_role[role] -= 1
        return missing_per_role

    def accepted_count(self):
        return sum(1 for x in self.roster_choices.values() if x == RosterStatus.ACCEPT)

    def set_roster_choice(self, player_name, roster_choice):
        if self.roster_choices.get(player_name, None) != roster_choice:
            self.updates_since_last_check.append((player_name, roster_choice))
        self.roster_choices[player_name] = roster_choice

    def check_updates(self):
        updates_since_last_check = self.updates_since_last_check
        self.updates_since_last_check = []
        return updates_since_last_check


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
