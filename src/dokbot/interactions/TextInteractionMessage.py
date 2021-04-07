from typing import Optional
from typing import Union, Any

import discord

from dokbot.DokBot import DokBot
from dokbot.DokBotContext import DokBotContext
from dokbot.entities.DiscordMessage import DiscordMessage
from exceptions.CancelInteractionException import CancelInteractionException
from exceptions.InternalBotException import InternalBotException
from exceptions.InvalidInputException import InvalidInputException
import asyncio

TRIES = 3


class TextInteractionMessage(DiscordMessage):
    def __init__(self, ctx: DokBotContext, content: str = None, embed: discord.Embed = None, *args,
                 **kwargs):
        super(TextInteractionMessage, self).__init__(ctx=ctx, embed=embed, content=content, *args,
                                                     **kwargs)
        # These variables will be filled once the message is sent
        self.channel_id = None
        self.recipient_id = None

    @classmethod
    async def interact(cls, ctx: DokBotContext, *args, **kwargs) -> Any:
        return await _interact(recipient=ctx.channel, message=cls(ctx=ctx, *args, **kwargs))

    async def get_response(self) -> Optional[str]:
        try:
            msg = await self.bot.wait_for('message', check=lambda response: _check_if_response(bot=self.ctx.bot, interaction_msg=self, msg=response), timeout=60)
            content = msg.content
            if content.strip() == '!skip':
                return None
            if content.strip() == '!done':
                raise CancelInteractionException("Stopping interaction")
            return content
        except asyncio.TimeoutError:
            raise CancelInteractionException("Operation timed out after one minute.")

    async def send_to(self, recipient: Union[discord.Member, discord.TextChannel]) -> discord.Message:
        msgs = await super(TextInteractionMessage, self).send_to(recipient)
        if len(msgs) != 1:
            raise InternalBotException("Unhandled case")
        msg = msgs[0]
        self.channel_id = msg.channel.id
        self.recipient_id = recipient.id
        return msg


def _check_if_response(bot: DokBot, interaction_msg: TextInteractionMessage, msg: discord.Message):
    assert interaction_msg.channel_id and interaction_msg.recipient_id, "There's no message to get a response for"
    return interaction_msg.channel_id == msg.channel.id and msg.author.id != bot.user.id


async def _interact(recipient, message: TextInteractionMessage) -> Any:
    await message.send_to(recipient)
    response = None
    finished = False
    trie = 0
    while not finished:
        try:
            response = await message.get_response()
            finished = True
        except InvalidInputException as ex:
            if trie >= TRIES:
                raise InvalidInputException("Exceeded retries, aborting interaction.")
            await recipient.send(content=str(ex))
            trie += 1

    return response
