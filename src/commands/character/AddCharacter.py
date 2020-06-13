from commands.character.CharacterCommand import CharacterCommand
from commands.utils.RegistrationHelper import register


class AddCharacter(CharacterCommand):
    @classmethod
    def subname(cls) -> str: return "add"

    @classmethod
    def description(cls) -> str: return "Add a new character"

    async def execute(self, **kwargs) -> None:
        await register(self.client, self.discord_guild, self.players_resource, self.member, allow_multiple_chars=True)
