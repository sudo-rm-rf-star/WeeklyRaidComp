import utils.Logger as Log
from commands.player.PlayerCommand import PlayerCommand
import discord


class AnnounceCommand(PlayerCommand):
    @classmethod
    def sub_name(cls) -> str: return "announce"

    @classmethod
    def argformat(cls) -> str: return "[announcement]"

    @classmethod
    def description(cls) -> str: return "Send an announcement to all of the raiders in your raiding group"

    async def execute(self, announcement: str, **kwargs) -> None:
        for raider in await self.get_raiders():
            try:
                await raider.send(content=announcement)
            except discord.Forbidden:
                Log.error(f'Received 403 when sending raid notification to {raider}')
