""" Utility class to help for raids with multiple rosters. """

from typing import Dict, List, Any
from logic.Character import Character
from logic.Player import Player
from logic.raid_composition.CompositionOptimizer import CompositionOptimizer
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus


class Roster:
    def __init__(self, raid_name: str, characters: List[Character] = None):
        self.raid_name = raid_name
        self.characters = characters if characters else []
        self.updated_since_last_check = False

    def get_team(self) -> List[Character]:
        return self.characters

    def compose(self) -> List[Character]:
        """ Creates/updates the different teams. Returns a list of updated players. """
        self.updated_since_last_check = True
        optimizer = CompositionOptimizer(self.raid_name, self.characters)
        return optimizer.make_raid_composition()

    def put_player(self, player: Player, roster_choice: RosterStatus = None, signee_choice: SignupStatus = None):

        selected_char = player.get_selected_char()
        # Remove previous player signups
        for character in player.characters:
            if selected_char != character:
                self.remove_character(character.name)

        self.updated_since_last_check = True

        try:
            i = self.characters.index(selected_char)
            selected_char = self.characters[i]
        except ValueError:
            i = len(self.characters)
            self.characters.append(selected_char)

        if roster_choice:
            selected_char.roster_status = roster_choice

        if signee_choice:
            selected_char.signup_status = signee_choice

        # Automatically decline anyone who is not accepted to the roster, and declined the raid.
        if selected_char.roster_status != RosterStatus.ACCEPT and selected_char.signup_status == RosterStatus.DECLINE:
            selected_char.roster_status = RosterStatus.DECLINE

        self.characters[i] = selected_char
        return selected_char

    def remove_character(self, player_name: str) -> bool:
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            'characters': [character.to_dict() for character in self.characters],
        }

    @staticmethod
    def from_dict(raid_name, item):
        return Roster(raid_name, [Character.from_dict(player) for player in item['characters']])
