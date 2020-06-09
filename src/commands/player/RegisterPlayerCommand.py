from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegistrationHelper import register
from utils.DiscordUtils import get_member


class RegisterPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = 'player'
        subname = 'register'
        description = 'Registreer iemand als raider. Stuurt een DM voor de registratie'
        super(RegisterPlayerCommand, self).__init__(subname=subname, description=description, argformat=argformat)

    async def execute(self, player: str, **kwargs) -> None:
        member = get_member(self.discord_guild, player)
        await register(self.client, self.discord_guild, self.players_resource, member, allow_multiple=False)
