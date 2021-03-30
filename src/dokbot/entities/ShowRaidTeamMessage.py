import discord
from dokbot.entities.DiscordMessage import DiscordMessage, field
from logic.RaidTeam import RaidTeam
from logic.Character import Character
from typing import List, Dict
from dokbot.RaidTeamContext import RaidTeamContext
from typing import Optional


class ShowRaidTeamMessage(DiscordMessage):
    @classmethod
    async def get_embed(cls, ctx: RaidTeamContext, **kwargs) -> Optional[discord.Embed]:
        players = ctx.get_raid_team_players()
        mains = [player.get_selected_char() for player in players]
        alts = [char for player in players for char in player.characters if char not in mains]
        embed = {'title': _get_title(ctx.raid_team),
                 'fields': await _get_fields(ctx, mains, alts),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)


async def _get_fields(ctx: RaidTeamContext, mains: List[Character], alts: List[Character]) -> List[Dict[str, str]]:
    fields = [_main_title_field(mains)]
    fields.extend(await DiscordMessage.show_characters(ctx=ctx, characters=mains))
    fields.append(_alt_title_field(alts))
    fields.extend(await DiscordMessage.show_characters(ctx=ctx, characters=alts))
    return fields


def _get_title(raid_team: RaidTeam) -> str:
    return str(raid_team)


def _main_title_field(mains: List[Character]):
    value = f'__**Mains ({len(mains)})**__'
    return field(value, inline=False)


def _alt_title_field(alts: List[Character]):
    value = f'__**Alts ({len(alts)})**__'
    return field(value, inline=False)
