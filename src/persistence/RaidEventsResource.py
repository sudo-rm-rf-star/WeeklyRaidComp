from utils.Singleton import Singleton
from .tables.TableFactory import TableFactory
from events.EventQueue import EventQueue
from events.raid.RaidEventCreated import RaidEventCreated
from events.raid.RaidEventUpdated import RaidEventUpdated
from events.raid.RaidEventRemoved import RaidEventRemoved
from datetime import datetime, timedelta
from logic.RaidEvent import RaidEvent
from typing import Optional
from logic.MessageRef import MessageRef
from exceptions.InvalidInputException import InvalidInputException
from utils.Constants import short_raid_names


class RaidEventsResource(metaclass=Singleton):
    def __init__(self):
        self.table = TableFactory().get_raid_events_table()
        self.queue = EventQueue()

    def create_raid(self, raid_name: str, raid_datetime: datetime, guild_id: int, team_name: str):
        raid_event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=guild_id, team_name=team_name)
        self.table.create_raid_event(raid_event)
        self.queue.send_event(RaidEventCreated(raid_event))
        return raid_event

    def get_raid(self, raid_name: str, raid_datetime: Optional[datetime], guild_id: int, team_name: str) -> RaidEvent:
        full_raid_name = short_raid_names[raid_name]
        if raid_datetime is None:
            since = datetime.now()
            until = datetime.now() + timedelta(weeks=4)
            raid_events = self.table.list_raid_events(raid_team_name=team_name, since=since, until=until)
            if len(raid_events) == 0:
                raise InvalidInputException(f'There are no raids in the upcoming four weeks for {full_raid_name}')
            raid_event = min(raid_events, key=lambda raid: raid.get_datetime())
        else:
            raid_event = self.table.get_raid_event(guild_id, team_name, raid_name, raid_datetime)
            if raid_event is None:
                raise InvalidInputException(f"There's no raid for {full_raid_name} on {raid_datetime}.")
        return raid_event

    def get_raid_by_message(self, message: MessageRef):
        return self.table.get_raid_event(raid_name=message.raid_name, raid_datetime=message.raid_datetime,
                                         team_name=message.team_name, guild_id=message.guild_id)

    def update_raid(self, raid_event: RaidEvent):
        self.table.update_raid_event(raid_event)
        self.queue.send_event(RaidEventUpdated(raid_event))

    """ A raid can only be removed as an event. We still need the initial raid event to ensure we can clean up the event properly. """
    def remove_raid(self, raid_event: RaidEvent) -> None:
        self.queue.send_event(RaidEventRemoved(raid_event))

    """ This may only be called from the handler for RaidEventRemoved """
    def delete_raid(self, raid_event: RaidEvent) -> None:
        self.table.remove_raid_event(raid_event)
