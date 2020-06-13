from commands.character.CharacterCommand import CharacterCommand


class SelectCharacter(CharacterCommand):
    @classmethod
    def subname(cls) -> str: return "select"

    @classmethod
    def argformat(cls) -> str: return "player"

    @classmethod
    def description(cls) -> str: return "Choose the character with which you want to sign up for raids"

    async def execute(self, player: str, **kwargs) -> None:
        success = self.players_resource.select_character(player, self.discord_guild.id)
        if success:
            self.respond(f'You will now sign up as {player} for raids. '
                         f'If you want to change the character with which you signed, please sign again for that raid.')
        else:
            self.respond(f'We could not find your character {player}. Perhaps you need to add it with the add '
                         f'character command')
