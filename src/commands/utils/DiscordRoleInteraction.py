from commands.utils.PlayerInteraction import InteractionMessage
from utils.DiscordUtils import get_roles, get_role
from exceptions.InvalidArgumentException import InvalidArgumentException
import discord


class DiscordRoleInteraction(InteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, *args, **kwargs):
        self.options = '/'.join([' '.join([role.name for role in get_roles(guild)])])
        content += f': [{self.options}]'
        self.guild = guild
        super().__init__(client, content, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordRoleInteraction, self).get_response()
        role = get_role(self.guild, response)
        if role:
            return response
        else:
            raise InvalidArgumentException(f'Please choose on of: {self.options}')
