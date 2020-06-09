from commands.character.CharacterCommand import CharacterCommand


class SelectCharacter(CharacterCommand):
    def __init__(self):
        argformat = "player"
        subname = 'select'
        description = 'Kies je huidige character waarmee je je inschrijft voor raids'
        super(SelectCharacter, self).__init__(subname=subname, description=description, argformat=argformat)

    async def execute(self, player: str, **kwargs) -> None:
        success = self.players_resource.select_character(player, self.discord_guild.id)
        if success:
            self.respond(f'You will now sign up as {player} for raids. '
                         f'If you want to change the character with which you signed, please sign again for that raid.')
        else:
            self.respond(f'We could not find your character {player}. Perhaps you need to add it with the add '
                         f'character command')
