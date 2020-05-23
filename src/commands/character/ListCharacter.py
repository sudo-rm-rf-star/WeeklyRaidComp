from commands.character.CharacterCommand import CharacterCommand
from utils.Constants import RAIDER_RANK
from client.entities.ShowCharactersMessage import ShowCharactersMessage


class AddCharacter(CharacterCommand):
    def __init__(self):
        argformat = ""
        subname = 'list'
        description = 'Toon je characters'
        super(AddCharacter, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, **kwargs) -> None:
        await ShowCharactersMessage(self.member, self.client, self.players_resource).send_to(self.member)

