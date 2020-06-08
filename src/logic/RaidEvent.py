from logic.Player import Player
from logic.enums.SignupStatus import SignupStatus
from logic.enums.RosterStatus import RosterStatus
from logic.Roster import Roster
from utils.Constants import abbrev_to_full
from utils.DateOptionalTime import DateOptionalTime
from utils.Date import Date
from utils.Time import Time
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier
from datetime import datetime
from typing import List, Dict, Any


class RaidEvent:
    def __init__(self, name: str, raid_datetime: DateOptionalTime, guild_id: int, group_id: int,
                 message_ids: List[DiscordMessageIdentifier] = None,
                 notification_ids: List[DiscordMessageIdentifier] = None, rosters=None, created_at: datetime = None,
                 updated_at: datetime = None):
        self.name = name
        self.guild_id = guild_id,
        self.group_id = group_id,
        self.datetime = raid_datetime
        self.message_ids = [] if not message_ids else message_ids  # Tuples of message ID, channel ID
        self.notification_ids = [] if not notification_ids else notification_ids  # Tuples of message ID, channel ID
        self.created_at = datetime.now() if not created_at else created_at
        self.updated_at = datetime.now() if not updated_at else updated_at
        self.roster = Roster(name) if not rosters else rosters

    def compose_roster(self) -> List[Player]:
        self.updated_at = datetime.now()
        return self.roster.compose()

    def add_to_signees(self, player: Player, signee_choice: SignupStatus) -> None:
        self.updated_at = datetime.now()
        self.roster.put_player(player=player, signee_choice=signee_choice)

    def add_to_roster(self, player: Player, roster_choice: RosterStatus, team_index: int = None) -> None:
        self.updated_at = datetime.now()
        self.roster.put_player(player=player, roster_choice=roster_choice, team_index=team_index)

    def remove_from_raid(self, player_name: str) -> bool:
        return self.roster.remove_player(player_name)

    def has_signed(self, player_name: str) -> bool:
        return any(player for player in self.roster.players if player.name == player_name)

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
                         raid_datetime=DateOptionalTime.from_timestamp(item['timestamp']),
                         guild_id=int(item['guild_id']),
                         group_id=int(item['group_id']),
                         message_ids=[DiscordMessageIdentifier.from_str(msg) for msg in item['message_ids']],
                         notification_ids=[DiscordMessageIdentifier.from_str(msg) for msg in item['notification_ids']],
                         created_at=datetime.fromtimestamp(item['created_at']),
                         updated_at=datetime.fromtimestamp(item['updated_at']),
                         rosters=Roster.from_dict(raid_name, item['roster']))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'guild_id': self.guild_id,
            'group_id': self.group_id,
            'timestamp': self.datetime.to_timestamp(),
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'roster': self.roster.to_dict(),
            'message_ids': [msg.to_str() for msg in self.message_ids],
            'notification_ids': [msg.to_str() for msg in self.notification_ids],
        }

    def __str__(self):
        return f'{self.get_name()}, {self.get_datetime()}'
