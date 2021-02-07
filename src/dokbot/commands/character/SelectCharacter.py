from dokbot.commands.character.CharacterCommand import CharacterCommand


class SelectCharacter(CharacterCommand):
    @classmethod
    def sub_name(cls) -> str: return "select"

    @classmethod
    def argformat(cls) -> str: return "character"

    @classmethod
    def description(cls) -> str: return "Choose the character with which you want to sign up for raids"

    async def execute(self, character: str, **kwargs) -> None:
        self.players_resource.select_character(self.player, character)
        self.respond(f'You will now sign up as {character} for raids. If you want to change the character with which you signed, please sign again for that '
                     f'raid.')
