from src.commands.raid.RaidCommand import RaidCommand
from src.client.GuildClient import GuildClient
from src.time.DateOptionalTime import DateOptionalTime
from src.logic.RaidEvents import RaidEvents
import discord
from src.common.Constants import OFFICER_RANK


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time"
        subname = 'remove'
        description = 'Verwijder een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname, description, argformat, OFFICER_RANK)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> str:
        return await self._run(client, message, **kwargs)

    async def _run(self, client: GuildClient, message: discord.Message, raid_name: str, raid_datetime: DateOptionalTime) -> str:
        raid_exists = RaidEvents().exists(raid_name, raid_datetime)
        if not raid_exists:
            return f'Raid event for {raid_name} on {raid_datetime} does not exist.'

        raid_event = RaidEvents().get(raid_name, raid_datetime)
        await RaidEvents().remove(client, raid_event)
        return f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully deleted.'
