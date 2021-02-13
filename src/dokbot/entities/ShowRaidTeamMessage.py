import discord
from dokbot.entities.DiscordMessage import DiscordMessage, field
from logic.Player import Player
from logic.RaidTeam import RaidTeam
from logic.Character import Character
from typing import List, Dict


class ShowRaidTeamMessage(DiscordMessage):
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, raid_team: RaidTeam,
                 embed: discord.Embed):
        self.discord_guild = discord_guild
        self.discord_client = discord_client
        self.raid_team = raid_team
        super().__init__(discord_client, discord_guild, embed=embed)

    @staticmethod
    async def create_message(discord_client: discord.Client, discord_guild: discord.Guild, raid_team: RaidTeam,
                             players: List[Player]):
        mains = [player.get_selected_char() for player in players]
        alts = [char for player in players for char in player.characters if char not in mains]
        embed = await _players_to_embed(client=discord_client, raid_team=raid_team, mains=mains, alts=alts)
        return ShowRaidTeamMessage(discord_client=discord_client, discord_guild=discord_guild, raid_team=raid_team,
                                   embed=embed)

    @staticmethod
    async def send_message(discord_client: discord.Client, discord_guild: discord.Guild, raid_team: RaidTeam,
                           players: List[Player], recipient):
        raid_msg = await ShowRaidTeamMessage.create_message(discord_client=discord_client, discord_guild=discord_guild,
                                                            raid_team=raid_team, players=players)
        return await raid_msg.send_to(recipient)


async def _players_to_embed(client: discord.Client, raid_team: RaidTeam, mains: List[Character],
                            alts: List[Character]) -> discord.Embed:
    embed = {'title': _get_title(raid_team),
             'fields': await _get_fields(client, mains, alts),
             'color': 2171428,
             'type': 'rich'}
    return discord.Embed.from_dict(embed)


async def _get_fields(client: discord.Client, mains: List[Character], alts: List[Character]) -> List[Dict[str, str]]:
    fields = [_main_title_field(mains)]
    fields.extend(await DiscordMessage.show_characters(client, mains))
    fields.append(_alt_title_field(alts))
    fields.extend(await DiscordMessage.show_characters(client, alts))
    return fields


def _get_title(raid_team: RaidTeam) -> str:
    return str(raid_team)


def _main_title_field(mains: List[Character]):
    value = f'__**Mains ({len(mains)})**__'
    return field(value, inline=False)


def _alt_title_field(alts: List[Character]):
    value = f'__**Alts ({len(alts)})**__'
    return field(value, inline=False)
