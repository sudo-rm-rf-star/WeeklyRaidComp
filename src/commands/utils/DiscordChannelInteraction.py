from commands.utils.PlayerInteraction import InteractionMessage
from utils.DiscordUtils import get_channel, get_channels
from exceptions.InvalidArgumentException import InvalidArgumentException
import discord


class DiscordChannelInteraction(InteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, *args, **kwargs):
        self.options = '/'.join([' '.join([role.name for role in get_channels(guild)])])
        content += f':\n [{self.options}]'
        self.guild = guild
        super().__init__(client, guild, content, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordChannelInteraction, self).get_response()
        channel = get_channel(self.guild, response)
        if channel:
            return response
        else:
            raise InvalidArgumentException(f'Please choose on of: {self.options}')
