from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegistrationHelper import register
from utils.DiscordUtils import get_member


class RegisterPlayerCommand(PlayerCommand):
    @classmethod
    def subname(cls) -> str: return "register"

    @classmethod
    def argformat(cls) -> str: return "player"

    @classmethod
    def description(cls) -> str: return "Register a new player for your team. Sends a PM to the player to register."

    async def execute(self, player: str, **kwargs) -> None:
        member = get_member(self.discord_guild, player)
        await register(self.client, self.guild, self.players_resource, member, allow_multiple_chars=False)
