from src.client.GuildClient import GuildClient
from src.client.entities.ShowPlayersMessage import ShowPlayersMessage
from src.commands.player.PlayerCommand import PlayerCommand
import discord


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = ''
        subname = 'showall'
        description = 'Toon een overzicht van alle raiders'
        super(RegisterPlayerCommand, self).__init__(subname, description, argformat)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> None:
        return await self._run(client, message)

    async def _run(self, client, message: discord.Message) -> None:
        destination = message.channel
        await ShowPlayersMessage(client).send_to(destination)
