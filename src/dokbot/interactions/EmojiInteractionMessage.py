from typing import Any
from typing import List
from typing import Optional

import discord

from dokbot.DokBotContext import DokBotContext
from dokbot.entities.DiscordMessage import DiscordMessage
from exceptions.InternalBotException import InternalBotException
from exceptions.CancelInteractionException import CancelInteractionException

import asyncio

TRIES = 3


class EmojiInteractionMessage(DiscordMessage):
    def __init__(self, ctx: DokBotContext, content: str, reactions: List[str], *args, **kwargs):
        super(EmojiInteractionMessage, self).__init__(ctx=ctx, content=content, reactions=reactions, *args, **kwargs)

    @classmethod
    async def interact(cls, ctx: DokBotContext, *args, **kwargs) -> Any:
        msg = cls(ctx=ctx, *args, **kwargs)
        await msg.send_to(ctx.channel)
        return await msg.get_response()

    @classmethod
    async def interact_with_author(cls, ctx: DokBotContext, *args, **kwargs) -> Any:
        msg = cls(ctx=ctx, *args, **kwargs)
        await msg.send_to(ctx.author)
        return await msg.get_response()

    async def get_response(self) -> Optional[str]:
        def check(reaction, user):
            try:
                return user.id == self.ctx.author.id and reaction.emoji.name in self.emojis
            except:
                return False
        try:
            (reaction, user) = await self.ctx.bot.wait_for('reaction_add', check=check, timeout=60)
            return reaction.emoji.name
        except asyncio.TimeoutError:
            raise CancelInteractionException("Operation timed out after one minute.")

    async def send_to(self, recipient) -> discord.Message:
        msgs = await super(EmojiInteractionMessage, self).send_to(recipient)
        if len(msgs) != 1:
            raise InternalBotException("Unhandled case")
        return msgs[0]
