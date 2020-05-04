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

    async def _run(self, client, message: discord.Message, member_name, role_name) -> None:
        all_members = set()
        if role_name:
            all_members = all_members.union(client.get_members_for_role(role_name))
        if member_name:
            all_members.add(client.get_member(member_name))

        if len(all_members) == 0:
            all_members.add(message.author)

        for member in all_members:
            await register(client, member, retry=len(all_members) == 1)



