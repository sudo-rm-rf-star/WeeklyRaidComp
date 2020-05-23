import discord
from client.entities.DiscordMessage import DiscordMessage
from client.PlayersResource import PlayersResource
from client.DiscordClient import DiscordClient
from client.entities.GuildMember import GuildMember
from utils.EmojiNames import ROLE_CLASS_EMOJI
from logic.Player import Player
from typing import List, Dict

EMPTY_FIELD = '\u200e'


class ShowCharactersMessage(DiscordMessage):
    def __init__(self, member: GuildMember, client: DiscordClient, players_resource: PlayersResource):
        self.client = client
        self.member = member
        self.players = players_resource.get_characters_by_id(member.id)
        self.selected_character = players_resource.get_character_by_id(member.id)
        self.embed = self._players_to_embed()
        super().__init__(embed=self.embed)

    def _players_to_embed(self) -> discord.Embed:
        embed = {
            'title': f'Characters van {self.member.display_name}',
            'fields': self._get_fields(),
            'color': 2171428,
            'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_fields(self) -> List[Dict[str, str]]:
        return [_field('\n'.join(sorted([self._get_player_line(player) for player in self.players])))]

    def _get_player_line(self, player: Player) -> str:
        selected_indicator = '**' if player == self.selected_character else ''
        return f'{self._role_class_emoji(player)} {selected_indicator}{player.name}{selected_indicator}'

    def _role_class_emoji(self, player: Player) -> discord.Emoji:
        return self._get_emoji(ROLE_CLASS_EMOJI[player.role][player.klass])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return self.client.get_emoji(name)


def _field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def _empty_field(inline: bool = True):
    return _field(EMPTY_FIELD, inline)
