from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegistrationHelper import register
from utils.DiscordUtils import get_member
from utils.Constants import RAIDER_RANK


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = 'player'
        subname = 'register'
        description = 'Registreer iemand als raider. Stuurt een DM voor de registratie'
        super(RegisterPlayerCommand, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, player: str, **kwargs) -> None:
        member = get_member(self.discord_guild, player)
        await register(self.client, self.players_resource, member, allow_multiple=False)
