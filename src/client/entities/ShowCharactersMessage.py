import discord
from client.entities.DiscordMessage import DiscordMessage
from client.PlayersResource import PlayersResource
from client.entities.GuildMember import GuildMember
from logic.Player import Player
from typing import List, Dict


class ShowCharactersMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, players_resource: PlayersResource, member: GuildMember):
        self.member = member
        self.players = players_resource.get_characters_by_id(member.id)
        self.selected_character = players_resource.get_character_by_id(member.id)
        super().__init__(client, guild, embed=self._players_to_embed())

    def _players_to_embed(self) -> discord.Embed:
        embed = {
            'title': f'Characters van {self.member.display_name}',
            'fields': self._get_fields(),
            'color': 2171428,
            'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_fields(self) -> List[Dict[str, str]]:
        return [self._field('\n'.join(sorted([self._get_player_line(player) for player in self.players])))]

    def _get_player_line(self, player: Player) -> str:
        selected_indicator = '**' if player == self.selected_character else ''
        return f'{self._role_class_emoji(player)} {selected_indicator}{player.name}{selected_indicator}'
