from persistence.TableFactory import TableFactory
from persistence.GuildsTable import GuildsTable
from logic.Guild import Guild
from logic.RaidGroup import RaidGroup
from logic.Player import Player
from typing import Optional, Tuple
import discord


class GuildsResource:
    def __init__(self, discord_client: discord.Client):
        self.discord_client = discord_client
        self.guilds_table: GuildsTable = TableFactory().get_guilds_table()

    def get_guild_and_group(self, player: Player) -> Tuple[Guild, Optional[RaidGroup]]:
        guild = self.guilds_table.get_guild(player.guild_id)
        groups = [group for group in guild.raid_groups if
                  group.group_id == player.selected_raidgroup_id or not player.selected_raidgroup_id]
        if len(groups) == 1:
            return guild, groups[0]
        return guild, groups[0] if len(groups) == 1 else None

    def create_guild(self):
        Guild()