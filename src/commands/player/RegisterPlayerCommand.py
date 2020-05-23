from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegisterPlayer import register
from utils.Constants import RAIDER_RANK
from typing import Optional


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = '[player][role]'
        subname = 'register'
        description = 'Registreer iemand als raider of iedereen met een bepaalde rol. Stuurt een DM voor de registratie'
        super(RegisterPlayerCommand, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, player: Optional[str] = None, role: Optional[str] = None, **kwargs) -> None:
        all_members = set()
        if not role or not player:
            self.respond("Please insert either a player and/or a role")
            return

        if role:
            all_members = all_members.union(self.client.get_members_for_role(role))
        if player:
            all_members.add(self.client.get_member(player))
        for member in all_members:
            await register(self.client, self.players_resource, member, allow_multiple=False)
