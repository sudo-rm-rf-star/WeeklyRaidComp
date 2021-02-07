import discord
from dokbot.entities.DiscordMessage import DiscordMessage
from logic.Player import Player
from logic.RaidTeam import RaidTeam
from typing import List, Dict


# TODO
class ShowRaidGroupsMessage(DiscordMessage):
    def __init__(self, client: discord.Client, discord_guild: discord.Guild, player: Player, raid_team: RaidTeam):
        self.raid_team = raid_team
        super().__init__(client, discord_guild, embed=self._players_to_embed())

    def _players_to_embed(self) -> discord.Embed:
        embed = {
            'title': f'Raid groups of {self.r.name} on {self.guild.realm}',
            'fields': self._get_fields(),
            'color': 2171428,
            'type': 'rich'}
        return discord.Embed.from_dict(embed)

    def _get_fields(self) -> List[Dict[str, str]]:
        return [self._field('\n'.join(sorted([self._get_raidgroup_line(raidgroup) for raidgroup in self.guild.raid_groups])))]

    def _get_raidgroup_line(self, raidgroup: RaidTeam) -> str:
        selected_id = self.player.selected_team_name if self.player.selected_team_name else -1
        selected_indicator = '**' if selected_id == raidgroup.id else ''
        return f'{selected_indicator}{raidgroup.name} ({raidgroup.raider_rank}){selected_indicator}'
