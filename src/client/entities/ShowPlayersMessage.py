import discord
from src.client.entities.DiscordMessage import DiscordMessage
from src.client.GuildClient import GuildClient
from src.common.EmojiNames import MISSING_EMOJI, SIGNUPS_EMOJI, ROLE_CLASS_EMOJI, ROLE_EMOJI, SIGNUP_STATUS_EMOJI
from src.common.Constants import RAIDER_RANK
from src.logic.enums.Role import Role
from src.logic.RaidEvents import RaidEvents
from src.logic.enums.SignupStatus import SignupStatus
from src.logic.enums.RosterStatus import RosterStatus
from src.logic.Players import Players
from src.logic.Player import Player
from discord import Embed
from typing import List, Dict, Union

EMPTY_FIELD = '\u200e'


class ShowPlayersMessage(DiscordMessage):
    def __init__(self, client: GuildClient):
        self.client = client
        self.players = Players().all()
        self.player_stats = RaidEvents().player_stats()
        self.embed = self._players_to_embed()
        super().__init__(embed=self.embed)

    def _players_to_embed(self) -> Embed:
        embed = {'title': self._get_title(),
                 'fields': self._get_fields(),
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)

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
        player_stats_for_role = {player: stats for player, stats in self.player_stats.items() if player.role == role}
        player_lines = '\n'.join(sorted([self._get_player_line(player, stats) for player, stats in player_stats_for_role.items()]))
        value = f'{self._role_emoji(role)} **__{role.name.capitalize()}__** ({len(player_stats_for_role.keys())}):\n{player_lines}'
        return _field(value, inline=False)

    def _get_player_line(self, player: Player, stats: Dict[Union[SignupStatus, RosterStatus], int]) -> str:
        return f'{self._role_class_emoji(player.name)} {player.name}: {self._get_stats_line(stats)}'

    def _get_stats_line(self, stats: Dict[Union[SignupStatus, RosterStatus], int]) -> str:
        formatted_stats = []
        for signup_status in iter(SignupStatus):
            formatted_stats.append(f'{stats.get(signup_status, 0)} {self._signup_choice_emoji(signup_status)}')
        # TODO: add roster_status
        return f"{', '.join(formatted_stats)}"

    def _get_missing_field(self) -> Dict[str, str]:
        value = 'Nog niet ingeschreven: '
        value += ', '.join([member.display_name for member in self.client.get_members_for_role(RAIDER_RANK)])
        return _field(value, inline=False)

    def _role_emoji(self, role: Role) -> discord.Emoji:
        return self._get_emoji(ROLE_EMOJI[role])

    def _role_class_emoji(self, player_name: str) -> discord.Emoji:
        player = Players().get(player_name)
        return self._get_emoji(ROLE_CLASS_EMOJI[player.role][player.klass])

    def _signup_choice_emoji(self, signup_choice: SignupStatus) -> discord.Emoji:
        return self._get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return self.client.get_emoji(name)


def _field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def _empty_field(inline: bool = True):
    return _field(EMPTY_FIELD, inline)
