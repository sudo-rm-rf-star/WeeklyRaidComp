import src.client.Logger as Log
from src.client.GuildClient import GuildClient
from src.common.Constants import RAIDER_RANK, MAINTAINER
from src.commands.player.PlayerCommand import PlayerCommand
import discord


class AnnounceCommand(PlayerCommand):
    def __init__(self):
        argformat = '[announcement]'
        subname = 'announce'
        description = 'Stuurt een aankondiging naar alle raiders'
        super(AnnounceCommand, self).__init__(subname, description, argformat)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> None:
        return await self._run(client, **kwargs)

    async def _run(self, client, announcement: str) -> None:
        raiders = client.get_members_for_role(RAIDER_RANK)
        for raider in raiders:
            try:
                await raider.send(content=announcement)
            except discord.Forbidden:
                Log.error(f'Received 403 when sending raid notification to {raider}')
