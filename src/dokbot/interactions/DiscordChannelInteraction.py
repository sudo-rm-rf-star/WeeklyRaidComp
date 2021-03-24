from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.DiscordUtils import get_channel, get_channels_non_async
from exceptions.InvalidInputException import InvalidInputException
from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from dokbot.DokBotContext import DokBotContext


ADD_CHANNEL = 'Add a new text channel.'


class DiscordChannelInteraction(OptionInteraction):
    def __init__(self, ctx: DokBotContext, content: str, *args, **kwargs):
        options = [role.name for role in get_channels_non_async(ctx.guild)] + [ADD_CHANNEL]
        super().__init__(ctx=ctx, options=options, content=content, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordChannelInteraction, self).get_response()
        if response == ADD_CHANNEL:
            msg = "Choose the name of your text channel."
            channel_name = await TextInteractionMessage.interact(ctx=self.ctx, content=msg)
            await self.ctx.guild.create_text_channel(channel_name)
            return channel_name
        channel = await get_channel(self.ctx.guild, response)
        if channel:
            return response
        else:
            raise InvalidInputException(f'Please choose on of: {self.options}')
