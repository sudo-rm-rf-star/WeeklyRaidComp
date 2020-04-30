from src.commands.roster.RosterCommand import RosterCommand
from src.exceptions.InternalBotException import InternalBotException
from src.common.Constants import OFFICER_RANK
from src.logic.RaidEvent import RaidEvent
from src.logic.RaidEvents import RaidEvents
from src.client.entities.RaidMessage import RaidMessage
from src.client.GuildClient import GuildClient
from src.time.DateOptionalTime import DateOptionalTime
from typing import Optional
import discord


class UpdateRosterCommand(RosterCommand):
    def __init__(self, subname: str, description: str):
        argformat = "raid_name player [raid_date][raid_time][team_index]"
        required_rank = OFFICER_RANK
        allow_trough_approval = True
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank,
                                            allow_trough_approval)

    def update_command(self, raid_event: RaidEvent, player_name: str, team_index: Optional[int]) -> None:
        raise InternalBotException("Please specify logic for this command.")

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> str:
        return await self._run(client, **kwargs)

    async def _run(self, client: GuildClient, raid_name: str, player: str, raid_datetime: Optional[DateOptionalTime], team_index: Optional[int]) -> str:
        raid_event = RaidEvents().get(raid_name, raid_datetime)
        self.update_command(raid_event, player, team_index)
        await RaidMessage(client, raid_event).sync()
        return f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully updated.'
