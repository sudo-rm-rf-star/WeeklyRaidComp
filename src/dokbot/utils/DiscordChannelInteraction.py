from dokbot.utils.OptionInteraction import OptionInteraction
from dokbot.DiscordUtils import get_channel, get_channels_non_async, create_channel
from exceptions.InvalidInputException import InvalidInputException
from dokbot.utils.PlayerInteraction import InteractionMessage
from dokbot.entities.GuildMember import GuildMember
import discord


ADD_CHANNEL = 'Add a new text channel.'


class DiscordChannelInteraction(OptionInteraction):
    def __init__(self, guild: discord.Guild, member: GuildMember, content: str, *args, **kwargs):
        self.member = member
        options = [role.name for role in get_channels_non_async(guild)] + [ADD_CHANNEL]
        super().__init__(guild=guild, options=options, content=content, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordChannelInteraction, self).get_response()
        if response == ADD_CHANNEL:
            msg = "Choose the name of your text channel."
            channel_name = await InteractionMessage.interact(member=self.member, client=self.client,
                                                             guild=self.discord_guild, content=msg)
            await self.discord_guild.create_text_channel(channel_name)
            return channel_name
        channel = await get_channel(self.guild, response)
        if channel:
            return response
        else:
            raise InvalidInputException(f'Please choose on of: {self.options}')
