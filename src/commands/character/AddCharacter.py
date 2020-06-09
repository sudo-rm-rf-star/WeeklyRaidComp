from commands.character.CharacterCommand import CharacterCommand
from commands.utils.RegistrationHelper import register


class AddCharacter(CharacterCommand):
    def __init__(self):
        subname = 'add'
        description = 'Voeg een character toe'
        super(AddCharacter, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        await register(self.client, self.discord_guild, self.players_resource, self.member, allow_multiple_chars=True)
