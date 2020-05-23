""" Utility class to help for raids with multiple rosters. """

from utils.Constants import player_count
from logic.RaidComposition import make_raid_composition, actual_vs_expected_per_role
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from typing import Dict, List, Any, Tuple
from logic.Player import Player
from collections import defaultdict


class Roster:
    def __init__(self, raid_name: str, players: List[Player] = None):
        self.raid_name = raid_name
        self.team_count = _team_count(raid_name)
        self.players = players if players else []
        self.updated_since_last_check = False

    def compose(self) -> List[Player]:
        """ Creates/updates the different teams. Returns a list of updated players. """
        self.updated_since_last_check = True
        updated_players = []
        for raid_team in self.team_iter():
            for player in make_raid_composition(self.raid_name, raid_team):
                updated_players.append(player)
        return updated_players

    def put_player(self, player: Player, roster_choice: RosterStatus = None, signee_choice: SignupStatus = None, team_index: int = None):
        self.updated_since_last_check = True

        try:
            i = self.players.index(player)
            player = self.players[i]
        except ValueError:
            i = len(self.players)
            self.players.append(player)

        team_index = team_index if team_index else player.team_index if player.team_index else self.get_optimal_team_index(player)
        player.team_index = team_index

        if roster_choice:
            player.roster_status = roster_choice

        if signee_choice:
            player.signup_status = signee_choice

        self.players[i] = player

    def remove_player(self, player_name: str) -> bool:
        self.updated_since_last_check = True
        players = [player for player in self.players if player.name == player_name]
        if len(players) == 0:
            return False
        player = players[0]
        self.players.remove(player)
        return True

    def was_updated(self) -> bool:
        if self.updated_since_last_check:
            self.updated_since_last_check = False
            return True
        return False

    def team_iter(self):
        return iter([player for player in self.players if player.team_index == team_index] for team_index in range(self.team_count))

    def get_optimal_team_index(self, player: Player) -> int:
        count_per_team_role_class = defaultdict(lambda: defaultdict(int))
        for raider in self.players:
            if raider.signup_status != SignupStatus.DECLINE:
                count_per_team_role_class[raider.team_index][(raider.role, raider.klass)] += 1
        return min(range(self.team_count), key=lambda team_index: count_per_team_role_class[team_index].get((player.role, player.klass), 0))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'players': [player.to_dict_for_raid_event() for player in self.players],
        }

    @staticmethod
    def from_dict(raid_name, item):
        return Roster(raid_name, [Player.from_dict(player) for player in item['players']])


def _team_count(raid_name: str) -> int:
    return 2 if player_count[raid_name] == 20 else 1
