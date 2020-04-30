from src.logic.enums.SignupStatus import SignupStatus
from src.logic.enums.RosterStatus import RosterStatus
from src.logic.Rosters import Rosters
from src.common.Constants import abbrev_to_full
from src.time.DateOptionalTime import DateOptionalTime
from src.time.Date import Date
from src.time.Time import Time
from datetime import datetime
from typing import Optional


class RaidEvent:
    def __init__(self, name: str, raid_datetime: DateOptionalTime, rosters=None):
        self.name = name
        self.datetime = raid_datetime
        self.message_id_pairs = set()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.rosters = Rosters(name) if not rosters else rosters

    def compose_roster(self) -> None:
        self.updated_at = datetime.now()
        return self.rosters.compose(self.name)

    def get_signup_choice(self, player_name: str) -> Optional[SignupStatus]:
        return self.rosters.signee_choices.get(player_name, None)

    def add_player_to_signees(self, player_name: str, signee_choice: SignupStatus) -> None:
        self.updated_at = datetime.now()
        self.rosters.add_signee(player_name, signee_choice)

    def add_player_to_roster(self, player_name: str, roster_choice: RosterStatus, team_index: int = None) -> None:
        self.updated_at = datetime.now()
        self.rosters.set_roster_choice(player_name, roster_choice, team_index)

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

    def get_signee_count(self) -> int:
        return len(self.rosters.signee_choices.keys())
