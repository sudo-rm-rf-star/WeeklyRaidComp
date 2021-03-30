from dokbot.interactions.OptionInteraction import OptionInteraction
from exceptions.InvalidInputException import InvalidInputException
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from dokbot.DokBotContext import DokBotContext
from typing import List
import discord

ADD_CHANNEL = 'Add a new text channel.'


class DiscordChannelInteraction(OptionInteraction):
    def __init__(self, ctx: DokBotContext, content: str, channels: List[discord.TextChannel], *args, **kwargs):
        self.channels = channels
        options = [channel.name for channel in channels] + [ADD_CHANNEL]
        super().__init__(ctx=ctx, options=options, content=content, *args, **kwargs)

    @classmethod
    async def interact(cls, ctx: DokBotContext, *args, **kwargs) -> discord.TextChannel:
        channels = [channel for channel in await ctx.guild.fetch_channels() if isinstance(channel, discord.TextChannel)]
        return await super(DiscordChannelInteraction, cls).interact(ctx=ctx, channels=channels, *args, **kwargs)

    async def get_response(self) -> discord.TextChannel:
        response = await super(DiscordChannelInteraction, self).get_response()
        if response == ADD_CHANNEL:
            msg = "Choose the name of your text channel."
            channel_name = await TextInteractionMessage.interact(ctx=self.ctx, content=msg)
            return await self.ctx.guild.create_text_channel(channel_name)
        channel = [channel for channel in self.channels if channel.name == response]
        if len(channel) == 1:
            return channel[0]
        else:
            raise InvalidInputException(f'Please choose on of: {self.options}')
