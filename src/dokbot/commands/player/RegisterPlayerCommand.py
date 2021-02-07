from dokbot.commands.player.PlayerCommand import PlayerCommand
from dokbot.utils.RegistrationHelper import register
from dokbot.DiscordUtils import get_member


class RegisterPlayerCommand(PlayerCommand):
    @classmethod
    def sub_name(cls) -> str: return "register"

    @classmethod
    def argformat(cls) -> str: return "player"

    @classmethod
    def description(cls) -> str: return "Register a new player for your team. Sends a PM to the player to register."

    async def execute(self, player: str, **kwargs) -> None:
        member = await get_member(self.discord_guild, player)
        await register(self.client, self.discord_guild, member, allow_multiple_chars=False)
