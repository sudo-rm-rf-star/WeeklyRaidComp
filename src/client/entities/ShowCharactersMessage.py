import discord
from client.entities.DiscordMessage import DiscordMessage
from client.PlayersResource import PlayersResource
from client.entities.GuildMember import GuildMember
from typing import List, Dict
from logic.Character import Character


class ShowCharactersMessage(DiscordMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, players_resource: PlayersResource, member: GuildMember):
        self.member = member
        self.player = players_resource.get_player_by_id(member.id)
        # Temp bugfix
        self.discord_client = client
        self.discord_guild = guild
        super().__init__(client, guild, embed=self._players_to_embed())

    def _players_to_embed(self) -> discord.Embed:
        embed = {
            'title': f'Characters van {self.member.display_name}',
            'fields': self._get_fields(),
            'color': 2171428,
            'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_fields(self) -> List[Dict[str, str]]:
        return [self._field('\n'.join(sorted([self._get_character_line(char) for char in self.player.characters])))]

    def _get_character_line(self, character: Character) -> str:
        selected_indicator = '**' if character == self.player.get_selected_char() else ''
        return f'{self._role_class_emoji(character)} {selected_indicator}{character.name}{selected_indicator}'
