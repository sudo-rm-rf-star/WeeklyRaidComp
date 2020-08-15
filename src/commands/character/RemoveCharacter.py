from commands.character.CharacterCommand import CharacterCommand


class RemoveCharacter(CharacterCommand):
    @classmethod
    def subname(cls) -> str: return "remove"

    @classmethod
    def description(cls) -> str: return "Remove your selected character"

    async def execute(self, character: str, **kwargs) -> None:
        self.players_resource.remove_character(self.player.get_selected_char())
        self.respond(f'Successfully removed {character}.')
