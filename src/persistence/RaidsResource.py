from utils.Singleton import Singleton
from .tables.TableFactory import TableFactory
from events.EventQueue import EventQueue
from events.raid.RaidEventCreated import RaidEventCreated
from datetime import datetime
from logic.RaidEvent import RaidEvent


class RaidsResource(metaclass=Singleton):
    def __init__(self):
        self.table = TableFactory().get_raid_events_table()
        self.queue = EventQueue()

    def create_raid(self, name: str, raid_datetime: datetime, guild_id: int, group_id: int):
        raid_event = RaidEvent(name=name, raid_datetime=raid_datetime, guild_id=guild_id, group_id=group_id)
        self.table.create_raid_event(raid_event)
        self.queue.send_event(RaidEventCreated(raid_event))
        return raid_event

