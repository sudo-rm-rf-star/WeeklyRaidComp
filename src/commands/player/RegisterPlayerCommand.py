from src.client.GuildClient import GuildClient
from src.commands.player.PlayerCommand import PlayerCommand
from src.commands.utils.RegisterPlayer import register
import discord


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = '[player][role]'
        subname = 'register'
        description = 'Registreer jezelf als raider, iemand anders of iedereen met een bepaalde rol. Stuurt een DM voor de registratie'
        super(RegisterPlayerCommand, self).__init__(subname, description, argformat)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> None:
        return await self._run(client, message, **kwargs)

    async def _run(self, client, message: discord.Message, player, role) -> None:
        all_members = set()
        if role:
            all_members = all_members.union(client.get_members_for_role(role))
        if player:
            all_members.add(client.get_member(player))

        if len(all_members) == 0:
            all_members.add(message.author)

        for member in all_members:
            await register(client, member, retry=len(all_members) == 1)



