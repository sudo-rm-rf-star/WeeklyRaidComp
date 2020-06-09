from commands.character.CharacterCommand import CharacterCommand
from client.entities.ShowCharactersMessage import ShowCharactersMessage


class AddCharacter(CharacterCommand):
    def __init__(self):
        subname = 'list'
        description = 'Toon je characters'
        super(AddCharacter, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        await ShowCharactersMessage(self.client, self.discord_guild, self.players_resource, self.member).send_to(self.member)

