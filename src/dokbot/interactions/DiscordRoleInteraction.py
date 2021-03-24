from dokbot.interactions.OptionInteraction import OptionInteraction
from exceptions.InvalidInputException import InvalidInputException
from dokbot.DiscordUtils import get_role, get_roles_non_async
from dokbot.DokBotContext import DokBotContext


class DiscordRoleInteraction(OptionInteraction):
    def __init__(self, ctx: DokBotContext, content: str, *args, **kwargs):
        options = [role.name for role in get_roles_non_async(ctx.guild)]
        super().__init__(ctx=ctx, content=content, options=options, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(DiscordRoleInteraction, self).get_response()
        role = await get_role(self.ctx.guild, response)
        if role:
            return response
        else:
            raise InvalidInputException(f'Please choose on of: {self.options}')
