""" Utility class to help for raids with multiple rosters. """

from typing import Dict, List, Any
from logic.Character import Character
from logic.Player import Player
from logic.raid_composition.CompositionOptimizer import CompositionOptimizer
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from typing import Optional
from exceptions.InternalBotException import InternalBotException
from datetime import datetime


class Roster:
    def __init__(self, raid_name: str, characters: List[Character] = None):
        self.raid_name = raid_name
        self.characters = characters if characters else []

    def get_team(self) -> List[Character]:
        return self.characters

    def compose(self) -> List[Character]:
        """ Creates/updates the different teams. Returns a list of updated players. """
        optimizer = CompositionOptimizer(self.raid_name, self.characters)
        return optimizer.make_raid_composition()

    def put_character(self, character: Character, roster_status: RosterStatus = None, signup_status: SignupStatus = None):
        try:
            i = self.characters.index(character)
            prev_character = self.characters[i]
            character.set_roster_status(prev_character.get_roster_status())
            character.set_signup_status(prev_character.get_signup_status())
        except ValueError:
            i = len(self.characters)
            self.characters.append(character)

        # Automatically decline anyone who is not accepted to the roster, and declined the raid.
        if character.get_roster_status() != RosterStatus.Accept and signup_status == SignupStatus.Decline:
            roster_status = RosterStatus.Decline

        # Automatically put anyone back to undecided if they accepted the raid after being declined to the roster
        if character.get_roster_status() == RosterStatus.Decline and signup_status != SignupStatus.Decline:
            roster_status = RosterStatus.Undecided

        if roster_status and roster_status != character.get_roster_status():
            character.set_roster_status(roster_status)

        if signup_status and signup_status != character.get_signup_status():
            character.set_signup_status(signup_status)

        self.characters[i] = character
        return character

    def remove_player(self, player: Player) -> None:
        self.characters = [character for character in self.characters if character.discord_id != player.discord_id]

    def get_signed_character(self, player: Player) -> Optional[Character]:
        if player is None:
            return None
        players = [char for char in self.characters if char.discord_id == player.discord_id]
        if len(players) == 0:
            return None
        if len(players) == 1:
            return players[0]
        raise InternalBotException(f'{player} in the event more than once.')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'characters': [character.to_dict() for character in self.characters],
        }

    @staticmethod
    def from_dict(raid_name, item):
        return Roster(raid_name, [Character.from_dict(player) for player in item['characters']])
