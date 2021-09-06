from dataclasses import dataclass
from typing import List

from events.Event import Event


@dataclass
class RosterUpdated(Event):
    def __init__(self, raid_token: str, character_ids: List[str]):
        self.raid_token = raid_token
        self.character_ids = character_ids
