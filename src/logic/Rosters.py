""" Utility class to help for raids with multiple rosters. """

from src.common.Constants import player_count
from src.logic.Roster import Roster
from collections import defaultdict
from src.logic.Players import Players
from src.logic.enums.RosterStatus import RosterStatus
from src.logic.enums.SignupStatus import SignupStatus
from src.logic.enums.Role import Role
from src.logic.enums.Class import Class
from typing import Dict, List, Optional, Tuple


class Rosters:
    def __init__(self, raid_name: str, rosters: List[Roster] = None, signee_choices: Dict[str, SignupStatus] = None, presence: List[str] = None):
        self.rosters = [Roster() for _ in range(_roster_count(raid_name))] if not rosters else rosters
        # Status as decided by the player
        self.signee_choices = {} if not signee_choices else signee_choices
        # Actual presence during the raid
        self.presence = set() if not presence else presence
        self.updated_since_last_check = False

    def compose(self, raid_name: str) -> None:
        self.updated_since_last_check = True
        if not self.rosters:
            self.rosters = [Roster() for _ in range(_roster_count(raid_name))]

        success = True
        for roster in self.rosters:
            success = success and roster.update(raid_name, self.signee_choices)
        return success

    def add_signee(self, player_name: str, signup_choice: SignupStatus) -> None:
        self.add_player(player_name, signup_choice=signup_choice)

    def set_roster_choice(self, player_name: str, roster_choice: RosterStatus, team_index: int = None):
        self.add_player(player_name, roster_choice=roster_choice, team_index=team_index)

    def add_player(self, player_name: str, roster_choice: RosterStatus = None, signup_choice: SignupStatus = None, team_index: int = None):
        self.updated_since_last_check = True
        team_and_roster_choice = self.get_team_and_roster_choice(player_name)

        if team_and_roster_choice:
            if roster_choice:
                team_index, old_roster_choice = team_and_roster_choice
                self.rosters[team_index].set_roster_choice(player_name, roster_choice)
        else:
            roster_choice = RosterStatus.UNDECIDED if not roster_choice else roster_choice
            team_index = self.find_best_roster_for_player(player_name) if not team_index else team_index
            self.rosters[team_index].set_roster_choice(player_name, roster_choice)

        if player_name not in self.signee_choices:
            self.signee_choices[player_name] = SignupStatus.UNDECIDED if signup_choice is None else signup_choice
        else:
            if signup_choice is not None:
                self.signee_choices[player_name] = signup_choice

    def get_roster_choice(self, player_name: str) -> Optional[RosterStatus]:
        return self.get_team_and_roster_choice(player_name)[1]

    def get_team_and_roster_choice(self, player_name: str) -> Optional[Tuple[int, RosterStatus]]:
        for i, roster in enumerate(self.rosters):
            if player_name in roster.roster_choices:
                return i, roster.roster_choices[player_name]
        return None

    def get_count_per_roster(self) -> Dict[int, Dict[Role, Dict[Class, int]]]:
        count_per_roster_role_class = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for i, roster in enumerate(self.rosters):
            for player_name in roster.roster_choices.keys():
                player = Players().get(player_name)
                count_per_roster_role_class[i][player.role][player.klass] += 1
        return count_per_roster_role_class

    def find_best_roster_for_player(self, player_name: str, count_per_roster_role_class: Dict[int, Dict[Role, Dict[Class, int]]] = None) -> int:
        player = Players().get(player_name)
        if count_per_roster_role_class is None:
            count_per_roster_role_class = self.get_count_per_roster()
        return min(range(len(self.rosters)), key=lambda j: count_per_roster_role_class[j][player.role][player.klass])

    def was_updated(self) -> bool:
        if self.updated_since_last_check:
            self.updated_since_last_check = False
            return True
        return False

    def check_roster_updates(self) -> List[Tuple[str, RosterStatus]]:
        updates = []
        for roster in self.rosters:
            for roster_update in roster.check_updates():
                updates.append(roster_update)
        return updates

    def __iter__(self):
        return iter(self.rosters)


def _roster_count(raid_name: str) -> int:
    return 2 if player_count[raid_name] == 20 else 1
