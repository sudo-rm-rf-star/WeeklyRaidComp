from logic.RaidEvent import RaidEvent
from dataclasses import dataclass
from .AbstractRaidEvent import AbstractRaidEvent


@dataclass
class RaidEventUpdated(AbstractRaidEvent):
    def __init__(self, raid_event: RaidEvent):
        super(RaidEventUpdated, self).__init__(raid_event)
