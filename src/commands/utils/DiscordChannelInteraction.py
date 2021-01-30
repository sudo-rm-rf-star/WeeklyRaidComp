from commands.utils.OptionInteraction import OptionInteraction
from utils.DiscordUtils import get_channel, get_channels_non_async
from exceptions.InvalidInputException import InvalidInputException
import discord


class DiscordChannelInteraction(OptionInteraction):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, *args, **kwargs):
        options = [role.name for role in get_channels_non_async(guild)]
        super().__init__(client, guild, content, options, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordChannelInteraction, self).get_response()
        channel = await get_channel(self.guild, response)
        if channel:
            return response
        else:
            raise InvalidInputException(f'Please choose on of: {self.options}')
