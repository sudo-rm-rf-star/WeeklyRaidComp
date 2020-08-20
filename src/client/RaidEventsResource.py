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
from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from logic.enums.SignupStatus import SignupStatus
from utils.DiscordUtils import get_emoji
from exceptions.InvalidArgumentException import InvalidArgumentException


class RaidEventsResource:
    def __init__(self, discord_client: discord.Client, messages_resource: MessagesResource):
        self.discord_client = discord_client
        self.events_table: RaidEventsTable = TableFactory().get_raid_events_table()
        self.messages_resource = messages_resource
        self.raid_cache = RaidEventsCache([raid_event for raid_event in self.events_table.scan() if
                                           raid_event.get_datetime() > DateOptionalTime.now()])

    async def create_raid(self, discord_guild: discord.Guild, group_id: int, raid_name: str,
                          raid_datetime: DateOptionalTime,
                          events_channel: discord.TextChannel, is_open: bool) -> Tuple[Optional[RaidEvent], str]:
        if self.raid_exists(discord_guild.id, group_id, raid_name, raid_datetime):
            return None, f'Raid event for {raid_name} on {raid_datetime} already exists.'
        if raid_datetime < DateOptionalTime.now():
            return None, f'Raid event must be in future'
        event = RaidEvent(name=raid_name, raid_datetime=raid_datetime, guild_id=discord_guild.id, group_id=group_id)
        await self.send_raid_message(discord_guild, events_channel, event, is_open)
        self.events_table.create_raid_event(event)
        self.raid_cache.update(event)
        return event, f'Raid event for {event.get_name()} on {event.get_datetime()} has been successfully created.'

    async def remove_raid(self, discord_guild: discord.Guild, raid_event: RaidEvent) -> None:
        self.delete_raid(raid_event)
        for message_ref in raid_event.message_refs:
            asyncio.create_task((await get_message(discord_guild, message_ref)).delete())

    def delete_raid(self, raid_event: RaidEvent) -> None:
        self.raid_cache.remove_if_exists(raid_event)
        self.events_table.remove_raid_event(raid_event)

    def update_raid(self, discord_guild: discord.Guild, raid_event: RaidEvent):
        self.raid_cache.update(raid_event)
        self.events_table.create_raid_event(raid_event)
        RaidMessage(self.discord_client, discord_guild, raid_event).sync()

    async def open_raid(self, discord_guild: discord.Guild, raid_event: RaidEvent):
        for message_ref in raid_event.message_refs:
            message = await get_message(discord_guild, message_ref)
            for emoji in [emoji_name for status, emoji_name in SIGNUP_STATUS_EMOJI.items() if
                          status != SignupStatus.UNDECIDED]:
                await message.add_reaction(emoji=get_emoji(discord_guild, emoji))

    def get_raid(self, discord_guild: discord.Guild, group_id: int, raid_name: str,
                 raid_datetime: Optional[DateOptionalTime]) -> Optional[RaidEvent]:
        raid_event = self.raid_cache.get(discord_guild.id, group_id, raid_name, raid_datetime)
        if raid_event is None:
            raid_event = self.events_table.get_raid_event(discord_guild.id, group_id, raid_name, raid_datetime)
            self.raid_cache.update(raid_event)
        return raid_event

    def get_raids(self, guild_id: int, group_id: int) -> List[RaidEvent]:
        return self.events_table.list_raid_events(guild_id, group_id)

    def get_raid_by_message(self, message: MessageRef):
        return self.events_table.get_raid_event(raid_name=message.raid_name, raid_datetime=message.raid_datetime,
                                                guild_id=message.guild_id,
                                                group_id=message.group_id)

    async def send_raid_message(self, discord_guild: discord.Guild, events_channel: discord.TextChannel,
                                raid_event: RaidEvent, is_open: bool) -> None:
        msg = await RaidMessage(self.discord_client, discord_guild, raid_event).send_to(events_channel)
        # There's probably some refactoring possible here.
        message_ref = MessageRef(message_id=msg.id, guild_id=discord_guild.id, channel_id=events_channel.id,
                                 raid_name=raid_event.name,
                                 raid_datetime=raid_event.datetime, group_id=raid_event.group_id)
        self.messages_resource.create_channel_message(message_id=msg.id, guild_id=discord_guild.id,
                                                      channel_id=msg.channel.id, raid_name=raid_event.name,
                                                      raid_datetime=raid_event.datetime, group_id=raid_event.group_id)
        raid_event.message_refs.append(message_ref)
        if is_open:
            await self.open_raid(discord_guild, raid_event)

    def raid_exists(self, guild_id: int, group_id: int, raid_name: str, raid_datetime: DateOptionalTime) -> bool:
        return self.events_table.get_raid_event(guild_id, group_id, raid_name, raid_datetime) is not None


class RaidEventsCache:
    def __init__(self, raid_events: List[RaidEvent]):
        self.upcoming_cache: Dict[int, Dict[int, Dict[str, Dict[DateOptionalTime, RaidEvent]]]] = defaultdict(
            lambda: defaultdict(dict))
        for raid_event in raid_events:
            self.update(raid_event)

    def remove_if_exists(self, raid_event: RaidEvent) -> bool:
        try:
            if raid_event == self.upcoming_cache[raid_event.guild_id][raid_event.group_id][raid_event.get_datetime()][
                raid_event.name]:
                del self.upcoming_cache[raid_event.guild_id][raid_event.group_id][raid_event.get_datetime()][
                    raid_event.name]
                return True
        except KeyError:
            pass
        return False

    def update(self, raid_event: RaidEvent):
        self.upcoming_cache[raid_event.guild_id][raid_event.group_id][raid_event.get_datetime()][
            raid_event.name] = raid_event

    def get(self, discord_guild: discord.Guild, group_id: int, raid_name: str,
            raid_datetime: Optional[DateOptionalTime]) -> Optional[RaidEvent]:
        try:
            upcoming_raids = self.upcoming_cache[discord_guild.id][group_id][raid_name]
            upcoming_datetime = raid_datetime if raid_datetime else min(upcoming_raids.keys(), key=lambda dt, _: dt)
            return upcoming_raids.get(upcoming_datetime, None)
        except KeyError:
            raise InvalidArgumentException(f'Failed to find raid for guild {discord_guild.id}, '
                                           f'group {group_id} and raid name {raid_name} on {raid_datetime}')
