from src.client.GuildClient import GuildClient
from src.commands.player.PlayerCommand import PlayerCommand
from src.commands.utils.RegisterPlayer import register
import discord


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = '[mentions]'
        subname = 'register'
        description = 'Registreer jezelf als raider of iemand anders door hem te mentionnen. Stuurt een DM voor de registratie'
        super(RegisterPlayerCommand, self).__init__(subname, description, argformat)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> str:
        return await self._run(client, message)

    async def _run(self, client, message: discord.Message) -> str:
        members_mentions = message.mentions
        role_mentions = message.role_mentions
        all_members = set()
        for role_mention in role_mentions:
            all_members = all_members.union(client.get_members_for_role(role_mention))
        for member_mention in members_mentions:
            all_members.add(member_mention)

        if len(all_members) == 0:
            all_members.add(message.author)

        for member in all_members:
            await register(client, member, retry=len(all_members) == 1)



