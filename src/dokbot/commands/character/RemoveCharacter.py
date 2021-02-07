from dokbot.commands.character.CharacterCommand import CharacterCommand


class RemoveCharacter(CharacterCommand):
    @classmethod
    def sub_name(cls) -> str: return "remove"

    @classmethod
    def description(cls) -> str: return "Remove your selected character"

    async def execute(self, **kwargs) -> None:
        character = self.player.get_selected_char()
        self.players_resource.remove_character(character)
        self.respond(f'Successfully removed {character}.')
