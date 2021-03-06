import asyncio
from collections import defaultdict
from typing import Optional, Dict, List

import discord

from client.MessagesResource import MessagesResource
from client.entities.RaidMessage import RaidMessage
from exceptions.InvalidInputException import InvalidInputException
from logic.MessageRef import MessageRef
from logic.RaidEvent import RaidEvent
from persistence.tables.RaidEventsTable import RaidEventsTable
from persistence.tables.TableFactory import TableFactory
from utils.Constants import abbrev_to_full
from utils.DiscordUtils import get_message
from datetime import datetime


class RaidEventsResource:
    def __init__(self, discord_client: discord.Client, messages_resource: MessagesResource):
        self.discord_client = discord_client
        self.events_table: RaidEventsTable = TableFactory().get_raid_events_table()
        self.messages_resource = messages_resource
        self.raid_cache = RaidEventsCache([raid_event for raid_event in self.events_table.scan() if
                                           raid_event.get_datetime() > datetime.now()])

    def create_raid(self, raid_event: RaidEvent):
        self.events_table.create_raid_event(raid_event)
        self.raid_cache.update(raid_event)

    async def remove_raid(self, discord_guild: discord.Guild, raid_event: RaidEvent) -> None:
        self.delete_raid(raid_event)
        for message_ref in raid_event.message_refs:
            asyncio.create_task((await get_message(discord_guild, message_ref)).delete())

    def delete_raid(self, raid_event: RaidEvent) -> None:
        self.raid_cache.remove_if_exists(raid_event)
        self.events_table.remove_raid_event(raid_event)

    def update_raid(self, discord_guild: discord.Guild, raid_event: RaidEvent):
        self.raid_cache.update(raid_event)
        self.events_table.update_raid_event(raid_event)
        RaidMessage(self.discord_client, discord_guild, raid_event).sync()

    def get_raid(self, discord_guild: discord.Guild, group_id: int, raid_name: str,
                 raid_datetime: Optional[datetime]) -> Optional[RaidEvent]:
        raid_event = self.raid_cache.get(discord_guild.id, group_id, raid_name, raid_datetime)
        if raid_event is None:
            raid_event = self.events_table.get_raid_event(discord_guild.id, group_id, raid_name, raid_datetime)
            if raid_event is None:
                raise InvalidInputException(f"There's no raid for {raid_name} on {raid_datetime}.")
            self.raid_cache.update(raid_event)
        return raid_event

    def get_raids(self, guild_id: int, group_id: int) -> List[RaidEvent]:
        return self.events_table.list_raid_events(guild_id, group_id)

    def get_raid_by_message(self, message: MessageRef):
        return self.events_table.get_raid_event(raid_name=message.raid_name, raid_datetime=message.raid_datetime,
                                                guild_id=message.guild_id,
                                                group_id=message.group_id)

    def raid_exists(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: datetime) -> bool:
        return self.events_table.get_raid_event(guild_id, group_id, raid_name, raid_datetime) is not None


class RaidEventsCache:
    def __init__(self, raid_events: List[RaidEvent]):
        self.upcoming_cache: Dict[int, Dict[int, Dict[str, Dict[datetime, RaidEvent]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict)))
        for raid_event in raid_events:
            self.update(raid_event)

    def remove_if_exists(self, raid_event: RaidEvent) -> bool:
        try:
            if raid_event == self.upcoming_cache[raid_event.guild_id][raid_event.team_id][raid_event.get_datetime()][raid_event.name]:
                del self.upcoming_cache[raid_event.guild_id][raid_event.team_id][raid_event.get_datetime()][
                    raid_event.name]
                return True
        except KeyError:
            pass
        return False

    def update(self, raid_event: RaidEvent):
        self.upcoming_cache[raid_event.guild_id][raid_event.team_id][raid_event.name][raid_event.datetime] = raid_event

    def get(self, guild_id: int, group_id: int, raid_name: str,
            raid_datetime: Optional[datetime]) -> Optional[RaidEvent]:
        try:
            upcoming_raids = self.upcoming_cache[guild_id][group_id][raid_name]
            upcoming_datetime = raid_datetime if raid_datetime else min(
                [dt for dt in upcoming_raids.keys() if dt > datetime.now()]
            )
            return upcoming_raids.get(upcoming_datetime, None)
        except (KeyError, ValueError):
            time_indication = f' on {raid_datetime}' if raid_datetime else ''
            raise InvalidInputException(f'Failed to find raid for {abbrev_to_full[raid_name]}{time_indication}')
