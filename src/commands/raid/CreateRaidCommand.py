from src.commands.raid.RaidCommand import RaidCommand
from src.client.GuildClient import GuildClient
from src.client.entities.RaidMessage import RaidMessage
from src.time.DateOptionalTime import DateOptionalTime
from src.logic.RaidEvent import RaidEvent
from src.logic.RaidEvents import RaidEvents
from typing import Optional
import discord
from src.common.Constants import OFFICER_RANK


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time [channel_name]"
        subname = 'create'
        description = 'Maak een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname, description, argformat, OFFICER_RANK)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> str:
        return await self._run(client, message, **kwargs)

    async def _run(self, client, message: discord.Message, raid_name: str, raid_datetime: DateOptionalTime, channel_name: Optional[str]) -> str:
        if channel_name:
            channel = client.get_channel(channel_name)
        else:
            channel = message.channel

        raid_exists = RaidEvents().exists(raid_name, raid_datetime)

        if raid_exists:
            return f'Raid event for {raid_name} on {raid_datetime} already exists.'

        raid_event = RaidEvent(raid_name, raid_datetime)
        # Ordering here is vital.
        await RaidMessage(client, raid_event).send_to(channel)
        RaidEvents().add(raid_event)
        return f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully created.'



