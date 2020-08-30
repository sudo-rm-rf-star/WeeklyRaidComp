from logic.Character import Character
from utils.DateOptionalTime import DateOptionalTime
from typing import Dict, Set, Optional, List
from exceptions.InternalBotException import InternalBotException
from utils.Constants import SUPPORTED_RAIDS


class Player:
    def __init__(self, *, discord_id: int, guild_id: int, characters: List[Character], selected_char: str, created_at: float,
                 present_dates: Optional[Dict[str, List[DateOptionalTime]]] = None, standby_dates: Optional[Dict[str, List[DateOptionalTime]]] = None,
                 selected_raidgroup_id: Optional[int] = None):
        self.discord_id = discord_id
        self.guild_id = guild_id
        self.characters = characters
        self.selected_char = selected_char
        self.present_dates = {} if not present_dates else present_dates
        self.created_at = created_at
        self.selected_raidgroup_id = None if not selected_raidgroup_id else selected_raidgroup_id
        self.standby_dates = {} if not standby_dates else standby_dates

    def add_standby_date(self, raid_name: str, raid_datetime: DateOptionalTime):
        if raid_name not in self.standby_dates:
            self.standby_dates[raid_name] = []
        if raid_datetime not in self.standby_dates[raid_name]:
            self.standby_dates[raid_name].append(raid_datetime)

    def add_present_date(self, raid_name: str, raid_datetime: DateOptionalTime):
        if raid_name not in self.present_dates:
            self.present_dates[raid_name] = []
        if raid_datetime not in self.present_dates[raid_name]:
            self.present_dates[raid_name].append(raid_datetime)

    def get_standby_counts(self) -> Dict[str, int]:
        return {raid_name: len(self.standby_dates[raid_name]) for raid_name in SUPPORTED_RAIDS}

    def get_selected_char(self) -> Character:
        for character in self.characters:
            if character.name == self.selected_char:
                return character
        raise InternalBotException("No character was selected")

    def set_selected_char(self, character_name: str):
        self.selected_char = character_name

    def __eq__(self, other) -> bool:
        return self.discord_id == other.discord_id

    def __hash__(self):
        return hash(self.discord_id)
