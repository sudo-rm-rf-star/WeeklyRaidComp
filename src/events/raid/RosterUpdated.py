from dataclasses import dataclass
from typing import Dict, Tuple

from events.Event import Event


@dataclass
class RosterUpdated(Event):
    def __init__(self, raid_token: str, roster_changes: Dict[int, Tuple[str, int]]):
        self.raid_token = raid_token
        self.roster_changes = roster_changes
