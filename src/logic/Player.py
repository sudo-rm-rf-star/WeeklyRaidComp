from src.logic.enums.Role import Role
from src.logic.enums.Class import Class
from src.logic.enums.Race import Race
from src.time.DateOptionalTime import DateOptionalTime
from typing import Dict, Set, Optional


class Player:
    def __init__(self, discord_id: int, char_name: str, klass: Class, role: Role, race: Race, present_dates: Optional[Dict[str, Set[DateOptionalTime]]] = None,
                 standby_dates: Optional[Dict[str, Set[DateOptionalTime]]] = None):
        self.discord_id = discord_id
        self.name = char_name
        self.klass = klass
        self.role = role
        self.race = race
        # These are based only on historical data
        self.present_dates = {} if not present_dates else present_dates
        self.standby_dates = {} if not standby_dates else standby_dates

    def add_standby_date(self, raid_name: str, raid_datetime: DateOptionalTime):
        if raid_name not in self.standby_dates:
            self.standby_dates[raid_name] = set()
        self.standby_dates[raid_name].add(raid_datetime)

    def add_present_date(self, raid_name: str, raid_datetime: DateOptionalTime):
        if raid_name not in self.present_dates:
            self.present_dates[raid_name] = set()
        self.present_dates[raid_name].add(raid_datetime)

    def get_standby_dates(self, raid_name: str) -> Set[DateOptionalTime]:
        return self.standby_dates.get(raid_name, set())

    def get_standby_count(self, raid_name: str) -> int:
        return len(self.get_standby_dates(raid_name))

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return f'{self.role.name.capitalize()} {self.klass.name.capitalize()} {self.name}'
