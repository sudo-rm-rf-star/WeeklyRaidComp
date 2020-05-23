from client.DiscordClient import DiscordClient
from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegisterPlayer import register
import discord
from typing import Optional


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = '[player][role]'
        subname = 'register'
        description = 'Registreer jezelf als raider, iemand anders of iedereen met een bepaalde rol. Stuurt een DM voor de registratie'
        super(RegisterPlayerCommand, self).__init__(subname, description, argformat)

    async def execute(self, player: Optional[str] = None, role: Optional[str] = None, **kwargs) -> None:
        all_members = set()
        if role:
            all_members = all_members.union(self.client.get_members_for_role(role))
        if player:
            all_members.add(self.client.get_member(player))

        if len(all_members) == 0:
            all_members.add(self.message.author)

        for member in all_members:
            await register(self.client, self.players_resource, member, retry=len(all_members) == 1)
