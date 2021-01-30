from logic.RaidEvent import RaidEvent
from events.Event import Event
from dataclasses import dataclass


@dataclass
class RaidEventCreated(Event):
    def __init__(self, raid_event: RaidEvent):
        self.guild_id = raid_event.guild_id
        self.group_id = raid_event.team_id
        self.raid_name = raid_event.name
        self.raid_datetime = raid_event.datetime
