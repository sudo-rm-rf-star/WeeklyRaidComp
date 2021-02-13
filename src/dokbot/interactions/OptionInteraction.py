from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from exceptions.InvalidInputException import InvalidInputException
import discord
from typing import List


class OptionInteraction(TextInteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, options: List[str], *args, **kwargs):
        self.guild = guild
        self.options = options
        self.options_str = "\n".join([f'{i+1}: {option}' for i, option in enumerate(options)])
        content = f'{content}\n{self.options_str}'
        super().__init__(client=client, guild=guild, content=content, *args, **kwargs)

    async def get_response(self) -> str:
        response = await super(OptionInteraction, self).get_response()
        try:
            i = int(response) - 1
            return self.options[i]
        except (ValueError, TypeError, IndexError):
            if response in self.options:
                return response
            raise InvalidInputException(f'Please choose on of:\n{self.options_str}')
