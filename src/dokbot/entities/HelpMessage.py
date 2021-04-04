from typing import List, Optional, Dict

import discord

from dokbot.DokBotContext import DokBotContext
from dokbot.entities.DiscordMessage import DiscordMessage, field
from utils.Constants import MAINTAINER_ID


class HelpMessage(DiscordMessage):
    @classmethod
    async def get_embed(cls, ctx: DokBotContext, **kwargs) -> Optional[discord.Embed]:
        actions = kwargs["actions"]
        embed = {'title': 'Info message',
                 'fields': await _get_fields(ctx=ctx, actions=actions),
                 'footer': await _get_footer(ctx),
                 'color': 2171428,
                 'type': 'rich'}
        return discord.Embed.from_dict(embed)


async def _get_footer(ctx: DokBotContext):
    maintainer = await ctx.bot.fetch_user(MAINTAINER_ID)
    return {'text': f"Want to report a bug or give feedback? Send a message to {maintainer}"}


async def _get_fields(ctx: DokBotContext, actions: list) -> List[Dict[str, str]]:
    fields = []
    for action in actions:
        emoji = await ctx.bot.emoji(action.name)
        entry = "{0} {1}".format(emoji, action.value)
        fields.append(field(entry, inline=False))
    return fields
