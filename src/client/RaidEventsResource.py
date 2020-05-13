from client.DiscordClient import DiscordClient
from client.entities.RaidMessage import RaidMessage
from client.entities.RaidNotification import RaidNotification
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier
from persistence.TableFactory import TableFactory
from persistence.RaidEventsTable import RaidEventsTable
from utils.DateOptionalTime import DateOptionalTime
from logic.RaidEvent import RaidEvent
from utils.Constants import EVENTS_CHANNEL, RAIDER_RANK
from typing import Optional, Dict, List
import utils.Logger as Log
import discord
import asyncio
from enum import Enum, auto


class CacheOperation(Enum):
    CREATE = auto()
    UPDATE = auto()
    REMOVE = auto()


class RaidEventsResource:
    def __init__(self, client: DiscordClient):
        self.client = client
        self.events_table: RaidEventsTable = TableFactory().get_raid_events_table()
        self.events_channel = None
        # Cache these to improve performance on hot keys
        self.upcoming_cache: Dict[str, RaidEvent] = {}
        # TODO: Optimization of this is possible by using timestamp as range and querying the time range rather than scanning
        for raid_event in self.events_table.scan():
            self._update_cache(raid_event, CacheOperation.CREATE)

    def on_ready(self):
        self.events_channel = self.client.get_channel(EVENTS_CHANNEL)

    async def create_raid(self, raid_name: str, raid_datetime: DateOptionalTime) -> str:
        if self.raid_exists(raid_name, raid_datetime):
            return f'Raid event for {raid_name} on {raid_datetime} already exists.'
        if raid_datetime < DateOptionalTime.now():
            return f'Raid event must be in future'
        event = RaidEvent(raid_name, raid_datetime)
        await self.send_raid_message(event)
        await self.send_raid_notification(event)
        self.events_table.put_raid_event(event)
        self._update_cache(event, CacheOperation.CREATE)
        return f'Raid event for {event.get_name()} on {event.get_datetime()} has been successfully created.'

    async def remove_raid(self, raid_name: str, raid_datetime: DateOptionalTime) -> str:
        raid_event = self.events_table.get_raid_event(raid_name, raid_datetime)
        if raid_event is None:
            return f'Raid event for {raid_name} on {raid_datetime} does not exist.'

        self.events_table.remove_raid_event(raid_name, raid_datetime)
        self._update_cache(raid_event, CacheOperation.REMOVE)
        for message_id in raid_event.message_ids:
            asyncio.create_task((await self.client.get_message(message_id)).remove())
        return f'Raid event for {raid_name} on {raid_datetime} has been successfully deleted.'

    def update_raid(self, raid_event: RaidEvent):
        self._update_cache(raid_event, CacheOperation.UPDATE)
        self.events_table.put_raid_event(raid_event)
        RaidMessage(self.client, raid_event).sync()

    def get_raid(self, raid_name: str, raid_datetime: Optional[DateOptionalTime]) -> Optional[RaidEvent]:
        if raid_datetime is None:
            raid_event = self.upcoming_cache.get(raid_name, None)
            return raid_event if raid_event and raid_event.get_datetime() > DateOptionalTime.now() else None
        return self.events_table.get_raid_event(raid_name, raid_datetime)

    def get_raids(self) -> List[RaidEvent]:
        return self.events_table.list_raid_events()

    def get_raid_by_notification_id(self, message_id: DiscordMessageIdentifier) -> Optional[RaidEvent]:
        return self.events_table.get_raid_event_by_message_id(message_id, True)

    def get_raid_by_message_id(self, message_id: DiscordMessageIdentifier) -> Optional[RaidEvent]:
        return self.events_table.get_raid_event_by_message_id(message_id, False)

    async def send_raid_notification(self, raid_event: RaidEvent) -> None:
        raiders = self.client.get_members_for_role(RAIDER_RANK)
        for raider in raiders:
            try:
                msg = await RaidNotification(self.client, raid_event).send_to(raider)
                raid_event.notification_ids.append(DiscordMessageIdentifier(msg.id, raider.id))
            except discord.Forbidden:
                Log.error(f'Received 403 when sending raid notification to {raider} for raid {raid_event}')

    async def send_raid_message(self, raid_event: RaidEvent) -> None:
        msg = await RaidMessage(self.client, raid_event).send_to(self.events_channel)
        raid_event.message_ids.append(DiscordMessageIdentifier(msg.id, self.events_channel.id))

    def raid_exists(self, raid_name: str, raid_datetime: DateOptionalTime) -> bool:
        return self.events_table.get_raid_event(raid_name, raid_datetime) is not None

    def _sync_cache(self):
        # TODO: Optimization of this is possible by using timestamp as range and querying the time range rather than scanning
        for raid_event in self.events_table.scan():
            self._update_cache(raid_event, CacheOperation.CREATE)

    def _update_cache(self, raid_event: RaidEvent, operation: CacheOperation):
        if operation == CacheOperation.REMOVE:
            if raid_event == self.upcoming_cache.get(raid_event.name):
                del self.upcoming_cache[raid_event.name]
                self._sync_cache()
        else:
            if raid_event.get_datetime() >= DateOptionalTime.now() and (raid_event.name not in self.upcoming_cache or self.upcoming_cache[raid_event.name].get_datetime() <= raid_event.get_datetime()):
                self.upcoming_cache[raid_event.name] = raid_event
