from typing import Optional

import discord

from logic.Guild import Guild
from logic.Player import Player
from logic.RaidGroup import RaidGroup
from persistence.GuildsTable import GuildsTable
from persistence.TableFactory import TableFactory


class GuildsResource:
    def __init__(self, discord_client: discord.Client):
        self.discord_client = discord_client
        self.guilds_table: GuildsTable = TableFactory().get_guilds_table()

    def get_guild(self, guild_id: int) -> Guild:
        return self.guilds_table.get_guild(guild_id)

    @staticmethod
    def get_group(guild: Guild, player: Player) -> Optional[RaidGroup]:
        if guild is None:
            return None
        groups = [group for group in guild.raid_groups if group.group_id == player.selected_raidgroup_id or not player.selected_raidgroup_id]
        return groups[0] if len(groups) == 1 else None

    def create_guild(self, guild: Guild) -> None:
        self.guilds_table.put_guild(guild)

    def update_guild(self, guild: Guild) -> None:
        self.guilds_table.put_guild(guild)
