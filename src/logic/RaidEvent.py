from logic.Player import Player
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from logic.Roster import Roster
from utils.Constants import abbrev_to_full
from utils.DateOptionalTime import DateOptionalTime
from utils.Date import Date
from utils.Time import Time
from datetime import datetime
from typing import List, Dict, Any, Optional
from logic.Character import Character
from logic.MessageRef import MessageRef


class RaidEvent:
    def __init__(self, name: str, raid_datetime: DateOptionalTime, guild_id: int, group_id: int, rosters=None,
                 created_at: datetime = None, updated_at: datetime = None, message_refs: List[MessageRef] = None,
                 is_open: bool = False, has_been_scanned: bool = False, report_code: Optional[str] = None,
                 presence: Optional[List[str]] = None):
        self.name = name
        self.guild_id = guild_id
        self.group_id = group_id
        self.datetime = raid_datetime
        self.created_at = datetime.now() if not created_at else created_at
        self.updated_at = datetime.now() if not updated_at else updated_at
        self.roster = Roster(name) if not rosters else rosters
        self.message_refs = [] if not message_refs else message_refs
        self.is_open = is_open

        # Data scanned for WL logs.
        self.has_been_scanned = has_been_scanned
        self.presence = presence if presence else []
        self.report_code = report_code if report_code else None

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

    def get_signed_characters(self) -> List[Character]:
        return self.roster.characters

    def get_signup_choice(self, player: Player) -> Optional[SignupStatus]:
        for char in self.get_signed_characters():
            if player.discord_id == char.discord_id:
                return char.signup_status
        return None

    def get_name(self, abbrev: bool = False) -> str:
        return self.name if abbrev else abbrev_to_full[self.name]

    def get_datetime(self) -> DateOptionalTime:
        return self.datetime

    def get_date(self) -> Date:
        return self.get_datetime().date

    def get_time(self) -> Time:
        return self.get_datetime().time

    def get_weekday(self) -> str:
        return self.get_datetime().weekday()

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        raid_name = item['name']
        return RaidEvent(name=raid_name,
                         raid_datetime=DateOptionalTime.from_timestamp(int(item['timestamp'])),
                         guild_id=int(item['guild_id']),
                         group_id=int(item['group_id']),
                         created_at=datetime.fromtimestamp(float(item['created_at'])),
                         updated_at=datetime.fromtimestamp(float(item['updated_at'])),
                         rosters=Roster.from_dict(raid_name, item['roster']),
                         message_refs=[MessageRef.from_dict(msg) for msg in item['message_refs']],
                         is_open=item.get('is_open', False),
                         presence=item.get('presence', None),
                         report_code=item.get('report_code', None),
                         has_been_scanned=item.get('has_been_scanned', False))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'guild_id': str(self.guild_id),
            'group_id': str(self.group_id),
            'timestamp': str(self.datetime.to_timestamp()),
            'created_at': str(self.created_at.timestamp()),
            'updated_at': str(self.updated_at.timestamp()),
            'roster': self.roster.to_dict(),
            'message_refs': [msg.to_dict() for msg in self.message_refs],
            'is_open': self.is_open,
            'presence': self.presence,
            'report_code': self.report_code,
            'has_been_scanned': self.has_been_scanned
        }

    def __str__(self):
        return f'{self.get_name()} on {self.get_datetime()} ({self.get_weekday().capitalize()})'
