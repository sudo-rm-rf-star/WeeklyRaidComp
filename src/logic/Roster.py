""" Utility class to help for raids with multiple rosters. """

from collections import defaultdict
from typing import Dict, List, Any

from logic.Character import Character
from logic.RaidComposition import make_raid_composition
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from utils.Constants import player_count


class Roster:
    def __init__(self, raid_name: str, characters: List[Character] = None):
        self.raid_name = raid_name
        self.team_count = _team_count(raid_name)
        self.characters = characters if characters else []
        self.updated_since_last_check = False

    def compose(self) -> List[Character]:
        """ Creates/updates the different teams. Returns a list of updated players. """
        self.updated_since_last_check = True
        updated_players = []
        for raid_team in self.team_iter():
            for character in make_raid_composition(self.raid_name, raid_team):
                updated_players.append(character)
        return updated_players

    def put_player(self, character: Character, roster_choice: RosterStatus = None, signee_choice: SignupStatus = None, team_index: int = None):
        self.updated_since_last_check = True

        try:
            i = self.characters.index(character)
            character = self.characters[i]
        except ValueError:
            i = len(self.characters)
            self.characters.append(character)

        team_index = team_index if team_index else character.team_index if character.team_index else self.get_optimal_team_index(character)
        character.team_index = team_index

        if roster_choice:
            character.roster_status = roster_choice

        if signee_choice:
            character.signup_status = signee_choice

        self.characters[i] = character

    def remove_player(self, player_name: str) -> bool:
        self.updated_since_last_check = True
        players = [player for player in self.characters if player.name == player_name]
        if len(players) == 0:
            return False
        player = players[0]
        self.characters.remove(player)
        return True

    def was_updated(self) -> bool:
        if self.updated_since_last_check:
            self.updated_since_last_check = False
            return True
        return False

    def team_iter(self):
        return iter([player for player in self.characters if player.team_index == team_index] for team_index in range(self.team_count))

    def get_optimal_team_index(self, character: Character) -> int:
        count_per_team_role_class = defaultdict(lambda: defaultdict(int))
        for raider in self.characters:
            if raider.signup_status != SignupStatus.DECLINE:
                count_per_team_role_class[raider.team_index][(raider.role, raider.klass)] += 1
        return min(range(self.team_count), key=lambda team_index: count_per_team_role_class[team_index].get((character.role, character.klass), 0))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'characters': [character.to_dict() for character in self.characters],
        }

    @staticmethod
    def from_dict(raid_name, item):
        return Roster(raid_name, [Character.from_dict(player) for player in item['characters']])


def _team_count(raid_name: str) -> int:
    return 2 if player_count[raid_name] == 20 else 1
