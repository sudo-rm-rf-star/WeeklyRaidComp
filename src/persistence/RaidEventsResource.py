from datetime import datetime, timedelta
from typing import List
from typing import Optional

from dokbot.DokBotContext import DokBotContext
from events.EventQueue import EventQueue
from events.raid.RaidEventCreated import RaidEventCreated
from events.raid.RaidEventRemoved import RaidEventRemoved
from events.raid.RaidEventUpdated import RaidEventUpdated
from exceptions.InvalidInputException import InvalidInputException
from logic.MessageRef import MessageRef
from logic.Raid import Raid
from logic.RaidEvent import RaidEvent
from .tables.TableFactory import TableFactory


class RaidEventsResource:
    def __init__(self, ctx: DokBotContext = None):
        self.table = TableFactory().get_raid_events_table()
        self.queue = EventQueue()
        self.ctx = ctx

    def create_raid(self, raid_name: str, raid_datetime: datetime, guild_id: int, team_name: str):
        raid_event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=guild_id, team_name=team_name)
        self.table.create_raid_event(raid_event)
        self.queue.send_event(RaidEventCreated(raid_event), ctx=self.ctx)
        return raid_event

    def list_raids_within_days(self, guild_id: int, team_name: str, days: int) -> List[RaidEvent]:
        since = datetime.now()
        until = datetime.now() + timedelta(days=days)
        return self.table.list_raid_events(guild_id=guild_id, raid_team_name=team_name, since=since, until=until)

    def get_raid(self, raid_name: str, raid_datetime: Optional[datetime], guild_id: int, team_name: str) -> RaidEvent:
        full_raid_name = Raid[raid_name].full_name
        if raid_datetime is None:
            days = 30
            raid_events = self.list_raids_within_days(guild_id=guild_id, team_name=team_name, days=30)
            if len(raid_events) == 0:
                raise InvalidInputException(f'There are no raids in the upcoming {days} days for {full_raid_name}')
            raid_event = min(raid_events, key=lambda raid: raid.get_datetime())
        else:
            raid_event = self.table.get_raid_event(guild_id, team_name, raid_name, raid_datetime)
            if raid_event is None:
                raise InvalidInputException(f"There's no raid for {full_raid_name} on {raid_datetime}.")
        return raid_event

    def get_raid_by_message(self, message: MessageRef):
        return self.table.get_raid_event(raid_name=message.raid_name, raid_datetime=message.raid_datetime,
                                         team_name=message.team_name, guild_id=message.guild_id)

    def synced(self, raid_event: RaidEvent) -> RaidEvent:
        return self.table.get_raid_event(raid_name=raid_event.name, raid_datetime=raid_event.datetime,
                                         team_name=raid_event.team_name, guild_id=raid_event.guild_id)

    def update_raid(self, raid_event: RaidEvent):
        self.table.update_raid_event(raid_event)
        self.queue.send_event(RaidEventUpdated(raid_event), ctx=self.ctx)

    def remove_raid(self, raid_event: RaidEvent) -> None:
        self.queue.send_event(RaidEventRemoved(raid_event), ctx=self.ctx)

    def delete_raid(self, raid_event: RaidEvent) -> None:
        self.table.remove_raid_event(raid_event)
