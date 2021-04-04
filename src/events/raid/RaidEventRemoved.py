from dataclasses import dataclass

from logic.RaidEvent import RaidEvent
from .AbstractRaidEvent import AbstractRaidEvent


@dataclass
class RaidEventRemoved(AbstractRaidEvent):
    def __init__(self, raid_event: RaidEvent):
        super().__init__(raid_event)
