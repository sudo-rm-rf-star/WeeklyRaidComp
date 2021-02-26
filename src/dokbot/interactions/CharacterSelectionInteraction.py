from logic.Player import Player
from logic.Character import Character
from dokbot.interactions.OptionInteraction import OptionInteraction
from exceptions.InvalidInputException import InvalidInputException
from dokbot.actions.Register import register
from dokbot.entities.discord.Member import discord.Member
import discord
from typing import Tuple

ADD_CHAR = 'Add a new character.'


class CharacterSelectionInteraction(OptionInteraction):
    def __init__(self, client: discord.Client, guild: discord.Guild, member: discord.Member, player: Player, *args, **kwargs):
        self.guild = guild
        self.player = player
        self.member = member

        options = [char.name for char in player.characters] + [ADD_CHAR]
        message = "Please choose the character you want to signup with for raids (Enter a number):"
        super().__init__(client, guild, message, options, *args, **kwargs)

    async def get_response(self) -> Tuple[Player, Character]:
        response = await super(CharacterSelectionInteraction, self).get_response()
        if response == ADD_CHAR:
            return await register(self.client, self.guild, self.member, allow_multiple_chars=True)
        for character in self.player.characters:
            if response == character.name:
                return self.player, character
        raise InvalidInputException(f'Please choose on of: {self.options}')
