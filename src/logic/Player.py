from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from logic.enums.Role import Role
from logic.enums.Class import Class
from logic.enums.Race import Race
from utils.DateOptionalTime import DateOptionalTime
from typing import Dict, Set, Optional, Any
from datetime import datetime


class Player:
    def __init__(self, char_name: str, klass: Class, role: Role, race: Race, discord_id: int, present_dates: Optional[Dict[str, Set[int]]] = None,
                 standby_dates: Optional[Dict[str, Set[int]]] = None, roster_status: Optional[RosterStatus] = None,
                 signup_status: Optional[SignupStatus] = None, team_index: Optional[int] = None, last_selected_time: Optional[datetime] = None):
        self.name = char_name
        self.klass = klass
        self.role = role
        self.race = race
        self.discord_id = discord_id
        # These will will not be filled for RaidEvents
        self.present_dates = {} if not present_dates else present_dates
        self.last_selected_time = None if not last_selected_time else last_selected_time
        # These will only be filled for RaidEvents
        self.standby_dates = {} if not standby_dates else standby_dates
        self.roster_status = roster_status if roster_status else RosterStatus.UNDECIDED
        self.signup_status = signup_status if signup_status else SignupStatus.UNDECIDED
        self.team_index = team_index

    def add_standby_date(self, raid_name: str, raid_datetime: DateOptionalTime):
        if raid_name not in self.standby_dates:
            self.standby_dates[raid_name] = set()
        self.standby_dates[raid_name].add(raid_datetime.to_timestamp())

    def add_present_date(self, raid_name: str, raid_datetime: DateOptionalTime):
        if raid_name not in self.present_dates:
            self.present_dates[raid_name] = set()
        self.present_dates[raid_name].add(raid_datetime.to_timestamp())

    def get_standby_dates(self, raid_name: str) -> Set[DateOptionalTime]:
        return set(DateOptionalTime.from_timestamp(timestamp) for timestamp in self.standby_dates.get(raid_name, set()))

    def get_present_dates(self, raid_name: str) -> Set[DateOptionalTime]:
        return set(DateOptionalTime.from_timestamp(timestamp) for timestamp in self.present_dates.get(raid_name, set()))

    def get_standby_count(self, raid_name: str) -> int:
        return len(self.get_standby_dates(raid_name))

    def is_declined(self) -> bool:
        return (self.signup_status == SignupStatus.DECLINE and self.roster_status != RosterStatus.ACCEPT) or self.roster_status == RosterStatus.DECLINE

    @staticmethod
    def from_dict(item: Dict[str, Any]):
        return Player(char_name=item['name'],
                      klass=Class[item['class']],
                      role=Role[item['role']],
                      race=Race[item['race']],
                      discord_id=item.get('discord_id', None),
                      standby_dates=item.get('standby_dates', None),
                      present_dates=item.get('present_dates', None),
                      roster_status=RosterStatus[item['roster_status']] if 'roster_status' in item else None,
                      signup_status=SignupStatus[item['signup_status']] if 'signup_status' in item else None,
                      team_index=item.get('team_index', None),
                      last_selected_time=datetime.fromtimestamp(item['last_selected_time']) if item.get('last_selected_time', None) else None)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'discord_id': self.discord_id,
            'class': self.klass.name,
            'role': self.role.name,
            'race': self.race.name,
            'present_dates': self.present_dates,
            'standby_dates': self.standby_dates,
            'last_selected_time': int(self.last_selected_time.timestamp())
        }

    def to_dict_for_raid_event(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'discord_id': self.discord_id,
            'class': self.klass.name,
            'role': self.role.name,
            'race': self.race.name,
            'roster_status': self.roster_status.name,
            'signup_status': self.signup_status.name,
            'team_index': self.team_index,
            'standby_dates': self.standby_dates
        }



    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return f'{self.role.name.capitalize()} {self.klass.name.capitalize()} {self.name}'

    def __hash__(self):
        return hash((self.name, self.discord_id))

