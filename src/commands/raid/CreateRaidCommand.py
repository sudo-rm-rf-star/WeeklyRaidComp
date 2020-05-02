from src.commands.raid.RaidCommand import RaidCommand
from src.client.GuildClient import GuildClient
from src.time.DateOptionalTime import DateOptionalTime
from src.logic.RaidEvent import RaidEvent
from src.logic.RaidEvents import RaidEvents
from typing import Optional
import discord
from src.common.Constants import OFFICER_RANK, RAIDER_RANK
import asyncio


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time [channel_name]"
        subname = 'create'
        description = 'Maak een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname, description, argformat, OFFICER_RANK)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> str:
        return await self._run(client, message, **kwargs)

    async def _run(self, client: GuildClient, message: discord.Message, raid_name: str, raid_datetime: DateOptionalTime, channel_name: Optional[str]) -> str:
        if channel_name:
            channel = client.get_channel(channel_name)
        else:
            channel = message.channel

        raid_exists = RaidEvents().exists(raid_name, raid_datetime)

        if raid_exists:
            return f'Raid event for {raid_name} on {raid_datetime} already exists.'
        if raid_datetime < DateOptionalTime.now():
            return f'Raid event must be in future'

        raid_event = RaidEvents().create(raid_name, raid_datetime)
        await RaidEvents().send_raid_message(client, channel, raid_event)
        await send_raid_notification(client, raid_event)
        return f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully created.'


async def send_raid_notification(client: GuildClient, raid_event: RaidEvent):
    raiders = client.get_members_for_role(RAIDER_RANK)
    raiders = [client.get_member('Dok')]
    for raider in raiders:
        await RaidEvents().send_raid_notification(client, raider, raid_event)
