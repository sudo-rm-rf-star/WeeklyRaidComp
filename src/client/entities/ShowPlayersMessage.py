import discord
from client.entities.DiscordMessage import DiscordMessage
from client.PlayersResource import PlayersResource
from utils.EmojiNames import SIGNUPS_EMOJI, ROLE_CLASS_EMOJI, ROLE_EMOJI, SIGNUP_STATUS_EMOJI
from utils.Constants import RAIDER_RANK
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.Player import Player
from typing import List, Dict

EMPTY_FIELD = '\u200e'


class ShowPlayersMessage(DiscordMessage):
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, players_resource: PlayersResource):
        self.discord_client = discord_client
        self.discord_guild = discord_guild
        self.players = players_resource.list_characters()
        self.embed = self._players_to_embed()
        super().__init__(embed=self.embed)

    def _players_to_embed(self) -> discord.Embed:
        embed = {'title': self._get_title(),
                 'fields': self._get_fields(),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_title(self) -> str:
        return f'{self._get_emoji(SIGNUPS_EMOJI)} {len(self.players)} geregistreerde kruisvaarder(s):'

    def _get_fields(self) -> List[Dict[str, str]]:
        fields = [
            self._get_field_for_role(Role.TANK),
            self._get_field_for_role(Role.HEALER),
            _empty_field(),

            self._get_field_for_role(Role.MELEE),
            self._get_field_for_role(Role.RANGED),
            _empty_field(),

            self._get_missing_field()  # Kruisvaarders who haven't registered
        ]
        return fields

    def _get_field_for_role(self, role: Role) -> Dict[str, str]:
        players_for_role = [player for player in self.players if player.role == role]
        player_lines = '\n'.join(sorted([self._get_player_line(player) for player in players_for_role]))
        value = f'{self._role_emoji(role)} **__{role.name.capitalize()}__** ({len(players_for_role)}):\n{player_lines}'
        return _field(value, inline=False)

    def _get_player_line(self, player: Player) -> str:
        return f'{self._role_class_emoji(player)} {player.name}'

    def _get_missing_field(self) -> Dict[str, str]:
        value = '**Nog niet ingeschreven:** '
        signed_ids = [player.discord_id for player in self.players]
        value += ', '.join([member.display_name for member in get_members_for_role(RAIDER_RANK) if member.id not in signed_ids])
        print(value)
        return _field(value, inline=False)

    def _role_emoji(self, role: Role) -> discord.Emoji:
        return self._get_emoji(ROLE_EMOJI[role])

    def _role_class_emoji(self, player: Player) -> discord.Emoji:
        return self._get_emoji(ROLE_CLASS_EMOJI[player.role][player.klass])

    def _signup_choice_emoji(self, signup_choice: SignupStatus) -> discord.Emoji:
        return self._get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return self.client.get_emoji(name)


def _field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def _empty_field(inline: bool = True):
    return _field(EMPTY_FIELD, inline)
