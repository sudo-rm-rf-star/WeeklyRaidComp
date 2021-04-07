from typing import List, Optional, Dict

import discord

from logic.Player import Player
from dokbot.DokBotContext import DokBotContext
from dokbot.entities.DiscordMessage import DiscordMessage, field
from datetime import datetime
from utils.Constants import DATETIME_FORMAT


class ShowPlayerMessage(DiscordMessage):
    @classmethod
    async def get_embed(cls, ctx: DokBotContext, **kwargs) -> Optional[discord.Embed]:
        player = kwargs['player']
        member = kwargs['member']
        embed = {'title': f"Player info for {member}",
                 'description': f'Also known as {member.display_name} in the server {ctx.guild}',
                 'fields': await _get_fields(ctx=ctx, player=player),
                 'footer': {'text': f'Player has registered at {datetime.fromtimestamp(player.created_at).strftime(DATETIME_FORMAT)}'},
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)


async def _get_fields(ctx: DokBotContext, player: Player) -> List[Dict[str, str]]:
    fields = []
    selected_char = player.get_selected_char()
    display_active_char = await ctx.bot.display_character(player.get_selected_char())
    fields.append(field(f'**Active character:**\n {display_active_char}', inline=False))
    other_chars = [char for char in player.characters if char != selected_char]
    if len(other_chars) > 0:
        display_other_chars = '\n'.join(
            ["**Other characters:**"] + [await ctx.bot.display_character(char) for char in other_chars])
        fields.append(field(display_other_chars, inline=False))
    return fields
