from logic.RaidEvent import RaidEvent
from events.Event import Event
from dataclasses import dataclass


@dataclass
class RaidEventUpdated(Event):
    def __init__(self, raid_event: RaidEvent):
        self.guild_id = raid_event.guild_id
        self.team_name = raid_event.team_name
        self.raid_name = raid_event.name
        self.raid_datetime = raid_event.datetime
