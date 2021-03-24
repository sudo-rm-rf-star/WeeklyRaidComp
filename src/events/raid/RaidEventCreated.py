from dataclasses import dataclass
from .AbstractRaidEvent import AbstractRaidEvent
from logic.RaidEvent import RaidEvent


@dataclass
class RaidEventCreated(AbstractRaidEvent):
    def __init__(self, raid_event: RaidEvent):
        super(RaidEventCreated, self).__init__(raid_event)
