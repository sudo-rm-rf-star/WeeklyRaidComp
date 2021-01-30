from commands.utils.PlayerInteraction import InteractionMessage
from exceptions.InvalidInputException import InvalidInputException
import discord
from typing import List


class OptionInteraction(InteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, message: str, options: List[str], *args, **kwargs):
        self.guild = guild
        self.options = options
        self.options_str = "\n".join([f'{i+1}: {option}' for i, option in enumerate(options)])
        content = f'{message}\n{self.options_str}'
        super().__init__(client, guild, content, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(OptionInteraction, self).get_response()
        try:
            i = int(response) - 1
            return self.options[i]
        except (ValueError, TypeError):
            if response in self.options:
                return response
            raise InvalidInputException(f'Please choose on of:\n{self.options_str}')
