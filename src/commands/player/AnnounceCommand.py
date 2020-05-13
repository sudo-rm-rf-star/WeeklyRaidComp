import utils.Logger as Log
from client.DiscordClient import DiscordClient
from utils.Constants import RAIDER_RANK
from commands.player.PlayerCommand import PlayerCommand
import discord


class AnnounceCommand(PlayerCommand):
    def __init__(self):
        argformat = '[announcement]'
        subname = 'announce'
        description = 'Stuurt een aankondiging naar alle raiders'
        super(AnnounceCommand, self).__init__(subname, description, argformat)

    async def execute(self, announcement: str, **kwargs) -> None:
        raiders = self.client.get_members_for_role(RAIDER_RANK)
        for raider in raiders:
            try:
                await raider.send(content=announcement)
            except discord.Forbidden:
                Log.error(f'Received 403 when sending raid notification to {raider}')
