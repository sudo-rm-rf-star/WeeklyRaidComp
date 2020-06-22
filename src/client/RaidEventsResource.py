import asyncio
from collections import defaultdict
from enum import Enum, auto
from typing import Optional, Dict, List, Tuple

import discord

from client.entities.RaidMessage import RaidMessage
from client.MessagesResource import MessagesResource
from logic.RaidEvent import RaidEvent
from logic.MessageRef import MessageRef
from persistence.RaidEventsTable import RaidEventsTable
from persistence.TableFactory import TableFactory
from utils.DateOptionalTime import DateOptionalTime
from utils.DiscordUtils import get_message


class CacheOperation(Enum):
    CREATE = auto()
    UPDATE = auto()
    REMOVE = auto()


class RaidEventsResource:
    def __init__(self, discord_client: discord.Client, messages_resource: MessagesResource):
        self.discord_client = discord_client
        self.events_table: RaidEventsTable = TableFactory().get_raid_events_table()
        self.messages_resource = messages_resource
        # Cache these to improve performance on hot keys
        self.upcoming_cache: Dict[int, Dict[int, Dict[str, RaidEvent]]] = defaultdict(lambda: defaultdict(dict))
        # TODO: Optimization of this is possible by using timestamp as range and querying the time range rather than scanning
        for raid_event in self.events_table.scan():
            self._update_cache(raid_event, CacheOperation.CREATE)

    async def create_raid(self, discord_guild: discord.Guild, group_id: int, raid_name: str, raid_datetime: DateOptionalTime,
                          events_channel: discord.TextChannel) -> Tuple[Optional[RaidEvent], str]:
        if self.raid_exists(discord_guild.id, group_id, raid_name, raid_datetime):
            return None, f'Raid event for {raid_name} on {raid_datetime} already exists.'
        if raid_datetime < DateOptionalTime.now():
            return None, f'Raid event must be in future'
        event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=discord_guild.id, group_id=group_id)
        await self.send_raid_message(discord_guild, events_channel, event)
        self.events_table.put_raid_event(event)
        self._update_cache(event, CacheOperation.CREATE)
        return event, f'Raid event for {event.get_name()} on {event.get_datetime()} has been successfully created.'

    async def remove_raid(self, discord_guild: discord.Guild, group_id: int, raid_name: str, raid_datetime: DateOptionalTime) -> str:
        raid_event = self.events_table.get_raid_event(discord_guild.id, group_id, raid_name, raid_datetime)
        if raid_event is None:
            return f'Raid event for {raid_name} on {raid_datetime} does not exist.'

        self.events_table.remove_raid_event(raid_name, raid_datetime)
        self._update_cache(raid_event, CacheOperation.REMOVE)
        for message_ref in raid_event.message_refs:
            asyncio.create_task((await get_message(discord_guild, message_ref)).remove())
        return f'Raid event for {raid_name} on {raid_datetime} has been successfully deleted.'

    def update_raid(self, discord_guild: discord.Guild, raid_event: RaidEvent):
        self._update_cache(raid_event, CacheOperation.UPDATE)
        self.events_table.put_raid_event(raid_event)
        RaidMessage(self.discord_client, discord_guild, raid_event).sync()

    def get_raid(self, discord_guild: discord.Guild, group_id: int, raid_name: str, raid_datetime: Optional[DateOptionalTime]) -> Optional[RaidEvent]:
        if raid_datetime is None:
            raid_event = self.upcoming_cache[discord_guild.id][group_id].get(raid_name, None)
            return raid_event if raid_event and raid_event.get_datetime() > DateOptionalTime.now() else None
        return self.events_table.get_raid_event(discord_guild.id, group_id, raid_name, raid_datetime)

    def get_raids(self, discord_guild: discord.Guild, group_id: int) -> List[RaidEvent]:
        return self.events_table.list_raid_events(discord_guild.id, group_id)

    def get_raid_by_message(self, message: MessageRef):
        return self.events_table.get_raid_event(raid_name=message.raid_name, raid_datetime=message.raid_datetime, guild_id=message.guild_id,
                                                group_id=message.group_id)

    async def send_raid_message(self, discord_guild: discord.Guild, events_channel: discord.TextChannel, raid_event: RaidEvent) -> None:
        msg = await RaidMessage(self.discord_client, discord_guild, raid_event).send_to(events_channel)
        message_ref = MessageRef(message_id=msg.id, guild_id=discord_guild.id, channel_id=events_channel.id, raid_name=raid_event.name,
                                 raid_datetime=raid_event.datetime, group_id=raid_event.group_id)
        raid_event.message_refs.append(message_ref)

    def raid_exists(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: DateOptionalTime) -> bool:
        return self.events_table.get_raid_event(guild_id, group_id, raid_name, raid_datetime) is not None

    def _update_cache(self, raid_event: RaidEvent, operation: CacheOperation):
        if operation == CacheOperation.REMOVE:
            if raid_event == self.upcoming_cache[raid_event.guild_id][raid_event.group_id].get(raid_event.name):
                del self.upcoming_cache[raid_event.guild_id][raid_event.group_id][raid_event.name]
        else:
            if raid_event.get_datetime() >= DateOptionalTime.now() and (
                    raid_event.name not in self.upcoming_cache[raid_event.guild_id][raid_event.group_id] or
                    raid_event.get_datetime() <= self.upcoming_cache[raid_event.guild_id][raid_event.group_id][raid_event.name].get_datetime()
            ):
                self.upcoming_cache[raid_event.guild_id][raid_event.group_id][raid_event.name] = raid_event
