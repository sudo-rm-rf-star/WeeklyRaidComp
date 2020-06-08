from commands.character.CharacterCommand import CharacterCommand
from utils.Constants import RAIDER_RANK
from commands.utils.RegistrationHelper import register


class AddCharacter(CharacterCommand):
    def __init__(self):
        argformat = ""
        subname = 'add'
        description = 'Voeg een character toe'
        super(AddCharacter, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, **kwargs) -> None:
        await register(self.client, self.players_resource, self.member, allow_multiple=True)
