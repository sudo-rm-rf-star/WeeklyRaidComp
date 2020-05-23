from commands.character import CharacterCommand
from utils.Constants import RAIDER_RANK


class AddCharacter(CharacterCommand):
    def __init__(self):
        argformat = ""
        subname = 'add'
        description = 'Voeg een character toe'
        super(AddCharacter, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, player: str, role: str, **kwargs) -> None:
        raise NotImplementedError()

