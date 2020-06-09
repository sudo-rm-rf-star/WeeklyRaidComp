import discord
from client.entities.DiscordMessage import DiscordMessage
from client.entities.GuildMember import GuildMember
from client.PlayersResource import PlayersResource
from utils.EmojiNames import SIGNUPS_EMOJI
from logic.enums.Role import Role
from logic.Character import Character
from typing import List, Dict

EMPTY_FIELD = '\u200e'


class ShowPlayersMessage(DiscordMessage):
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, players_resource: PlayersResource, raiders: List[GuildMember]):
        self.players = players_resource.list_players(discord_guild.id)
        self.characters = [char for player in self.players for char in player.characters]
        self.embed = self._players_to_embed()
        self.raiders = raiders
        super().__init__(discord_client, discord_guild, embed=self.embed)

    def _players_to_embed(self) -> discord.Embed:
        embed = {'title': self._get_title(),
                 'fields': self._get_fields(),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_title(self) -> str:
        return f'{self._get_emoji(SIGNUPS_EMOJI)} {len(self.characters)} geregistreerde kruisvaarder(s):'

    def _get_fields(self) -> List[Dict[str, str]]:
        fields = [
            self._get_field_for_role(Role.TANK),
            self._get_field_for_role(Role.HEALER),
            self._empty_field(),

            self._get_field_for_role(Role.MELEE),
            self._get_field_for_role(Role.RANGED),
            self._empty_field(),

            self._get_missing_field()  # Kruisvaarders who haven't registered
        ]
        return fields

    def _get_field_for_role(self, role: Role) -> Dict[str, str]:
        chars_for_role = [char for char in self.characters if char.role == role]
        player_lines = '\n'.join(sorted([self._get_char_line(char) for char in chars_for_role]))
        value = f'{self._role_emoji(role)} **__{role.name.capitalize()}__** ({len(chars_for_role)}):\n{player_lines}'
        return self._field(value, inline=False)

    def _get_char_line(self, character: Character) -> str:
        return f'{self._role_class_emoji(character)} {character.name}'

    def _get_missing_field(self) -> Dict[str, str]:
        value = '**Nog niet ingeschreven:** '
        signed_ids = [player.discord_id for player in self.players]
        value += ', '.join([member.display_name for member in self.raiders if member.id not in signed_ids])
        print(value)
        return self._field(value, inline=False)
