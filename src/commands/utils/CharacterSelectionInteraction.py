from logic.Player import Player
from logic.Character import Character
from commands.utils.OptionInteraction import OptionInteraction
from exceptions.InternalBotException import InternalBotException
from commands.utils.RegistrationHelper import register
from client.PlayersResource import PlayersResource
from client.entities.GuildMember import GuildMember
import discord
from typing import Tuple

ADD_CHAR = 'Add a new character.'


class CharacterSelectionInteraction(OptionInteraction):
    def __init__(self, client: discord.Client, guild: discord.Guild, players_resource: PlayersResource,
                 member: GuildMember, player: Player, *args, **kwargs):
        self.guild = guild
        self.player = player
        self.member = member
        self.players_resource = players_resource

        options = [char.name for char in player.characters] + [ADD_CHAR]
        message = "Please choose the character you want to signup with for raids (Enter a number):"
        super().__init__(client, guild, message, options, *args, **kwargs)

    async def get_response(self) -> Tuple[Player, Character]:
        response = await super(CharacterSelectionInteraction, self).get_response()
        if response == ADD_CHAR:
            return await register(self.client, self.discord_guild, self.players_resource, self.member,
                                  allow_multiple_chars=True)
        for character in self.player.characters:
            if response == character.name:
                return self.player, character
        raise InternalBotException(f"Could not find character {response} for {self.player}")
