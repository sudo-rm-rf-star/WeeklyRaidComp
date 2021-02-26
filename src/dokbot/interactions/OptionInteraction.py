from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from exceptions.InvalidInputException import InvalidInputException
from discord.ext.commands import Context
from dokbot.entities.DiscordMessage import field, DiscordMessage
from dokbot.DokBotContext import DokBotContext
from typing import List
from discord import Embed
from dokbot.DokBot import DokBot
import discord


class OptionInteraction(TextInteractionMessage):
    def __init__(self, ctx: DokBotContext, content: str, options: List[str], *args, **kwargs):
        self.options = list(options)
        embed = self._get_embed(content=content, options=options)
        super().__init__(ctx=ctx, embed=embed, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(OptionInteraction, self).get_response()
        try:
            i = int(response) - 1
            return self.options[i]
        except (ValueError, TypeError, IndexError):
            if response in self.options:
                return response
            raise InvalidInputException(f'Please choose one of the given options.')

    def _get_embed(self, content: str, options: List[str]):
        embed = {'title': content,
                 'fields': [field('\n'.join([f'{i+1}:\t{option}' for i, option in enumerate(options)]), inline=False)],
                 'color': 2171428,
                 'type': 'rich'}
        return Embed.from_dict(embed)

