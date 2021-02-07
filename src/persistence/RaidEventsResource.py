from utils.Singleton import Singleton
from .tables.TableFactory import TableFactory
from events.EventQueue import EventQueue
from events.raid.RaidEventCreated import RaidEventCreated
from events.raid.RaidEventUpdated import RaidEventUpdated
from events.raid.RaidEventRemoved import RaidEventRemoved
from datetime import datetime
from logic.RaidEvent import RaidEvent
from typing import Optional
from logic.MessageRef import MessageRef
from exceptions.InvalidInputException import InvalidInputException
from utils.Constants import abbrev_to_full
from typing import Dict
from collections import defaultdict
from persistence.tables.RaidEventsTable import RaidEventsTable


class RaidEventsResource(metaclass=Singleton):
    def __init__(self):
        self.table = TableFactory().get_raid_events_table()
        self.queue = EventQueue()
        self.raid_cache = RaidEventsCache(self.table)

    def create_raid(self, raid_name: str, raid_datetime: datetime, guild_id: int, team_name: str):
        raid_event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=guild_id, team_name=team_name)
        self.table.create_raid_event(raid_event)
        self.queue.send_event(RaidEventCreated(raid_event))
        return raid_event

    def get_raid(self, raid_name: str, raid_datetime: datetime, guild_id: int, team_name: str) -> Optional[RaidEvent]:
        raid_event = self.raid_cache.get(guild_id, team_name, raid_name, raid_datetime)
        if raid_event is None:
            if raid_datetime:
                raise InvalidInputException(f'There are no raids in the future for {abbrev_to_full[raid_name]}')
            else:
                raise InvalidInputException(f"There's no raid for {abbrev_to_full[raid_name]} on {raid_datetime}.")
        return raid_event

    def get_raid_by_message(self, message: MessageRef):
        return self.table.get_raid_event(raid_name=message.raid_name, raid_datetime=message.raid_datetime,
                                         team_name=message.team_name, guild_id=message.guild_id)

    def update_raid(self, raid_event: RaidEvent):
        self.raid_cache.update(raid_event)
        self.queue.send_event(RaidEventUpdated(raid_event))

    def delete_raid(self, raid_event: RaidEvent) -> None:
        self.raid_cache.remove(raid_event)
        self.queue.send_event(RaidEventRemoved(raid_event))


class RaidEventsCache:
    def __init__(self, table: RaidEventsTable):
        self.upcoming_cache: Dict[int, Dict[int, Dict[str, Dict[datetime, RaidEvent]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict)))
        self.table = table
        for raid_event in self.table.scan():
            if raid_event.get_datetime() > datetime.now():
                self.upcoming_cache[raid_event.guild_id][raid_event.team_name][raid_event.name][
                    raid_event.datetime] = raid_event

    def remove(self, raid_event: RaidEvent) -> bool:
        self.table.remove_raid_event(raid_event)
        try:
            del self.upcoming_cache[raid_event.guild_id][raid_event.team_name][raid_event.get_datetime()][raid_event.name]
        except KeyError:
            pass
        return False

    def update(self, raid_event: RaidEvent):
        self.upcoming_cache[raid_event.guild_id][raid_event.team_name][raid_event.name][
            raid_event.datetime] = raid_event
        self.table.update_raid_event(raid_event)

    def get(self, guild_id: int, team_name: str, raid_name: str,
            raid_datetime: Optional[datetime]) -> Optional[RaidEvent]:
        try:
            upcoming_raids = self.upcoming_cache[guild_id][team_name][raid_name]
            upcoming_datetime = raid_datetime if raid_datetime else min(
                [dt for dt in upcoming_raids.keys() if dt > datetime.now()]
            )
            raid_event = upcoming_raids.get(upcoming_datetime)
            if not raid_event:
                raid_event = self.table.get_raid_event(guild_id=guild_id, team_name=team_name, raid_name=raid_name,
                                                       raid_datetime=raid_datetime)
                if raid_event:
                    self.update(raid_event)
            return raid_event
        except (KeyError, ValueError):
            return None
