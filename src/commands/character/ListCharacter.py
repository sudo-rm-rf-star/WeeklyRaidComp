from commands.character.CharacterCommand import CharacterCommand
from client.entities.ShowCharactersMessage import ShowCharactersMessage


class ListCharacter(CharacterCommand):
    @classmethod
    def sub_name(cls) -> str: return "list"

    @classmethod
    def description(cls) -> str: return "List all your characters"

    async def execute(self, **kwargs) -> None:
        await ShowCharactersMessage(self.client, self.discord_guild, self.players_resource, self.member).send_to(self.member)
