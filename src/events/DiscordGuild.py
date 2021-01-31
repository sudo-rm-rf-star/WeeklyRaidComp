from utils.DiscordUtils import *
from logic.Guild import Guild
from logic.RaidTeam import RaidTeam
from persistence.tables.PlayersTable import PlayersTable
from typing import Optional, Set
import logging


class DiscordGuild:
    def __init__(self, client: discord.Client, discord_guild: discord.Guild, guild: Guild,
                 raid_group: RaidTeam = None):
        self.discord_client = client
        self.guild = guild
        self.discord_guild = discord_guild
        self.id = discord_guild.id
        self.raid_group: Optional[RaidTeam] = None
        if raid_group:
            self.raid_group = raid_group
        elif len(guild.raid_groups) == 1:
            self.raid_group = guild.raid_groups[0]

    async def get_events_channel(self) -> discord.TextChannel:
        return await get_channel(self.discord_guild, self.raid_group.events_channel)

    async def get_raiders(self) -> Set[GuildMember]:
        raiders = []
        try:
            async for member in self.discord_guild.fetch_members(limit=None):
                if member and any(role.name == self.raid_group.raider_rank for role in member.roles):
                    raiders.append(GuildMember(member, self.discord_guild.id))
        except discord.Forbidden:
            logging.getLogger().error(f'There are non-transient problems with Discord permissions...')
        return set(raiders)

    async def get_autoinvited_raiders(self, players_table: PlayersTable) -> Set[GuildMember]:
        raiders = await self.get_raiders()
        for player in players_table.list_players(self.guild):
            if player.autoinvited:
                member = self.discord_guild.get_member(player.discord_id)
                if member:
                    raiders.add(GuildMember(member, self.guild.id))
        return set(raiders)


async def create_helper(client: discord.Client, guild: Guild, raid_group: RaidTeam = None) -> DiscordGuild:
    discord_guild = await client.fetch_guild(guild.id)
    return DiscordGuild(client, discord_guild, guild, raid_group)
