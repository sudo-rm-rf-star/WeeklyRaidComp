import discord
from client.entities.DiscordMessage import DiscordMessage
from logic.Player import Player
from logic.Guild import Guild
from logic.RaidTeam import RaidTeam
from typing import List, Dict


class ShowRaidGroupsMessage(DiscordMessage):
    def __init__(self, client: discord.Client, discord_guild: discord.Guild, player: Player, guild: Guild):
        self.guild = guild
        self.player = player
        super().__init__(client, discord_guild, embed=self._players_to_embed())

    def _players_to_embed(self) -> discord.Embed:
        embed = {
            'title': f'Raid groups van {self.guild.name} op {self.guild.realm}',
            'fields': self._get_fields(),
            'color': 2171428,
            'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_fields(self) -> List[Dict[str, str]]:
        return [self._field('\n'.join(sorted([self._get_raidgroup_line(raidgroup) for raidgroup in self.guild.raid_groups])))]

    def _get_raidgroup_line(self, raidgroup: RaidTeam) -> str:
        selected_id = self.player.selected_raidgroup_id if self.player.selected_raidgroup_id else -1
        selected_indicator = '**' if selected_id == raidgroup.id else ''
        return f'{selected_indicator}{raidgroup.name} ({raidgroup.raider_rank}){selected_indicator}'
