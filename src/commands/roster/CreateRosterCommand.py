from src.commands.roster.RosterCommand import RosterCommand
from src.client.entities.RaidMessage import RaidMessage
from src.client.GuildClient import GuildClient
from src.logic.RaidEvents import RaidEvents
from src.time.DateOptionalTime import DateOptionalTime
import discord


class CreateRosterCommand(RosterCommand):
    def __init__(self):
        argformat = "raid_name [raid_date][raid_time]"
        subname = 'create'
        description = 'Maak een raid compositie voor een event'
        super(RosterCommand, self).__init__('roster', subname, description, argformat)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> str:
        return await self._run(client, **kwargs)

    async def _run(self, client: GuildClient, raid_name: str, raid_datetime: DateOptionalTime) -> str:
        raid_event = RaidEvents().get(raid_name, raid_datetime)
        success = raid_event.compose_roster()
        await RaidMessage(client, raid_event).sync()
        success_indicator = 'successfully' if success else 'unsuccessfully'
        return f'Roster for {raid_event.get_name()} on {raid_event.get_datetime()} has been {success_indicator} updated.'
