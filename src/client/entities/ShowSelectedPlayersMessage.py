import discord
from client.entities.DiscordMessage import DiscordMessage
from client.entities.GuildMember import GuildMember
from utils.EmojiNames import SIGNUPS_EMOJI
from logic.enums.Role import Role
from logic.Player import Player
from logic.Character import Character
from typing import List, Dict

EMPTY_FIELD = '\u200e'

MAX_CHARACTERS_PER_ROLE = 10  # Any field has a max amount of 1024 characters


class ShowSelectedPlayersMessage(DiscordMessage):
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, players: List[Player], raiders: List[GuildMember]):
        self.discord_guild = discord_guild
        self.discord_client = discord_client
        self.raiders = raiders
        self.raider_ids = [raider.id for raider in raiders]
        self.players = [player for player in players if player.discord_id in self.raider_ids]
        self.characters = [player.get_selected_char() for player in self.players]
        signed_ids = [player.discord_id for player in self.players]
        self.unsigned_members = [member.display_name for member in self.raiders if member.id not in signed_ids]
        self.embed = self._players_to_embed()
        super().__init__(discord_client, discord_guild, embed=self.embed)

    def _players_to_embed(self) -> discord.Embed:
        embed = {'title': self._get_title(),
                 'fields': self._get_fields(),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_title(self) -> str:
        return f'{self._get_emoji(SIGNUPS_EMOJI)} {len(self.characters)} geregistreerde kruisvaarder(s), enkel geselecteerde characters:'

    def _get_fields(self) -> List[Dict[str, str]]:
        fields = []
        for role in [Role.TANK, Role.HEALER, Role.MELEE, Role.RANGED]:
            fields.extend(self._get_field_for_role(role))
        if len(self.unsigned_members) > 0:
            fields.append(self._get_missing_field())
        return fields

    def _get_field_for_role(self, role: Role) -> List[Dict[str, str]]:
        chars_for_role = sorted([char for char in self.characters if char.role == role], key=lambda char: str(char.klass))
        i = 0
        fields = []
        while i < len(chars_for_role):
            chars = chars_for_role[i:i + MAX_CHARACTERS_PER_ROLE]
            player_lines = '\n'.join([self._get_char_line(char) for char in chars])
            if i == 0:
                value = f'{self._role_emoji(role)} **__{role.name.capitalize()}__** ({len(chars_for_role)}):\n{player_lines}'
                fields.append(self._field(value, inline=True))
            else:
                value = player_lines
                fields.append(self._field(value, inline=True))
            i += MAX_CHARACTERS_PER_ROLE
        while len(fields) % 3 != 0:
            fields.append(self._empty_field(inline=True))
        return fields

    def _get_char_line(self, character: Character) -> str:
        return f'{self._role_class_emoji(character)} {character.name}'

    def _get_missing_field(self) -> Dict[str, str]:
        value = '**Not yet registered:** '
        value += ', '.join(self.unsigned_members)
        return self._field(value, inline=False)
