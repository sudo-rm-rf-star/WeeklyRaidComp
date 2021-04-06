from logic.Player import Player
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from logic.enums.Class import Class
from logic.enums.Role import Role
from logic.Roster import Roster
from utils.Constants import full_raid_names
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from logic.Character import Character
from logic.MessageRef import MessageRef
import arrow


class RaidEvent:
    def __init__(self, name: str, raid_datetime: datetime, guild_id: int, team_name: str,
                 roster=None, created_at: datetime = None, updated_at: datetime = None,
                 message_refs: List[MessageRef] = None, is_open: bool = False):
        self.name = name
        self.guild_id = guild_id
        self.team_name = team_name
        self.datetime = raid_datetime
        self.timestamp = int(raid_datetime.timestamp())
        self.created_at = datetime.now() if not created_at else created_at
        self.updated_at = datetime.now() if not updated_at else updated_at
        self.roster = Roster(name) if not roster else roster
        self.message_refs = [] if not message_refs else message_refs
        self.is_open = is_open

    def compose_roster(self) -> List[Character]:
        self.updated_at = datetime.now()
        return self.roster.compose()

    def add_to_signees(self, player: Player, signee_choice: SignupStatus) -> Character:
        self.updated_at = datetime.now()
        signed_character = self.roster.get_signed_character(player)
        selected_character = player.get_selected_char()
        if signed_character and signed_character != selected_character:
            self.roster.remove_player(player)
        return self.roster.put_character(character=selected_character, signup_status=signee_choice)

    def add_to_roster(self, player: Player, roster_choice: RosterStatus) -> Character:
        self.updated_at = datetime.now()
        character = self.roster.get_signed_character(player)
        if character is None:
            character = player.get_selected_char()
        character = player.get_char(character.name)
        return self.roster.put_character(character=character, roster_status=roster_choice)

    def has_char_signed(self, character: Character) -> bool:
        return any(char for char in self.roster.characters if char == character)

    def has_user_signed(self, user_id: int) -> bool:
        return any(char for char in self.roster.characters if char.discord_id == user_id)

    def has_user_signed_as(self, user_id: int, signup_status: SignupStatus) -> bool:
        return any(char for char in self.roster.characters if
                   char.discord_id == user_id and char.get_signup_status() == signup_status)

    def get_signed_characters(self) -> List[Character]:
        return self.roster.characters

    def get_characters(self, role: str = None, klass: str = None, signup_choice=None, roster_choice=None):
        if signup_choice and isinstance(signup_choice, str):
            signup_choice = SignupStatus[signup_choice.upper()]
        if roster_choice and isinstance(roster_choice, str):
            roster_choice = RosterStatus[roster_choice.upper()]

        return sorted([
            char for char in self.get_signed_characters() if
            (not role or char.get_role() == Role[role.upper()]) and
            (not klass or char.klass == Class[klass.upper()]) and
            (not signup_choice or char.get_signup_status() == signup_choice) and
            (not roster_choice or char.get_roster_status() == roster_choice)
        ], key=lambda char: (char.get_role, char.klass, char.get_roster_status().name, char.get_signup_status().name, char.name))

    def get_signup_choice(self, player: Player) -> Optional[SignupStatus]:
        for char in self.get_signed_characters():
            if player.discord_id == char.discord_id:
                return char.get_signup_status()
        return SignupStatus.Unknown

    def is_invited(self, player: Player) -> bool:
        for char in self.get_signed_characters():
            if player.discord_id == char.discord_id:
                return True
        return False

    def get_name(self, abbrev: bool = False) -> str:
        return self.name if abbrev else full_raid_names[self.name]

    def in_future(self) -> bool:
        return self.datetime > datetime.now()

    def get_datetime(self) -> datetime:
        return self.datetime

    def get_date(self) -> date:
        return self.get_datetime().date()

    def get_time(self) -> str:
        return self.get_datetime().time().strftime("%H:%M")

    def get_weekday(self) -> str:
        return self.get_datetime().strftime("%A")

    def get_month(self) -> str:
        return self.get_datetime().strftime("%B")

    def relative_time(self):
        return arrow.get(self.datetime).humanize()

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        raid_name = item['name']
        return RaidEvent(name=raid_name,
                         raid_datetime=datetime.fromtimestamp(int(item['timestamp'])),
                         guild_id=int(item['guild_id']),
                         team_name=item['team_name'],
                         created_at=datetime.fromtimestamp(float(item['created_at'])),
                         updated_at=datetime.fromtimestamp(float(item['updated_at'])),
                         roster=Roster.from_dict(raid_name, item['roster']),
                         message_refs=[MessageRef.from_dict(msg) for msg in item['message_refs']],
                         is_open=item.get('is_open', False))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'guild_id': str(self.guild_id),
            'team_name': str(self.team_name),
            'timestamp': int(self.datetime.timestamp()),
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'roster': self.roster.to_dict(),
            'message_refs': [msg.to_dict() for msg in self.message_refs],
            'is_open': self.is_open
        }

    def __str__(self):
        return f'{self.get_name()} on {self.get_date()} {self.get_time()} ({self.get_weekday().capitalize()})'
