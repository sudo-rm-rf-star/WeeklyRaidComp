import discord

from dokbot.interactions.OptionInteraction import OptionInteraction
from exceptions.InvalidInputException import InvalidInputException
from dokbot.DiscordUtils import get_role, get_roles_non_async


class DiscordRoleInteraction(OptionInteraction):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, *args, **kwargs):
        options = [role.name for role in get_roles_non_async(guild)]
        super().__init__(client, guild, content, options, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordRoleInteraction, self).get_response()
        role = await get_role(self.guild, response)
        if role:
            return response
        else:
            raise InvalidInputException(f'Please choose on of: {self.options}')
