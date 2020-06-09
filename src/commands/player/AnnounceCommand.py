import utils.Logger as Log
from commands.player.PlayerCommand import PlayerCommand
import discord


class AnnounceCommand(PlayerCommand):
    def __init__(self):
        argformat = '[announcement]'
        subname = 'announce'
        description = 'Stuurt een aankondiging naar alle raiders'
        super(AnnounceCommand, self).__init__(subname=subname, description=description, argformat=argformat)

    async def execute(self, announcement: str, **kwargs) -> None:
        for raider in self.get_raiders():
            try:
                await raider.send(content=announcement)
            except discord.Forbidden:
                Log.error(f'Received 403 when sending raid notification to {raider}')
