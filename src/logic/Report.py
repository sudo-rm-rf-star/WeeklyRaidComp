from dataclasses import dataclass
from typing import Set, List
from typing import Dict


@dataclass
class Fight:
    name: str
    start_time: int  # Start time of fight in seconds relative to start of report
    end_time: int  # End time of fight in seconds relative to start of report
    present_players: Set[str]


@dataclass
class Report:
    code: str
    fights: List[Fight]
    buff_counts: Dict[str, Dict[str, int]]  # For a given buff, count the amount of occurrences on any player

    def get_url(self):
        return f'https://classic.warcraftlogs.com/reports/{self.code}'
