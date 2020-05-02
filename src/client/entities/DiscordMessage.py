import discord
from typing import Union


class DiscordMessage:
    def __init__(self, content: str = None, embed: discord.Embed = None):
        self.content = content
        self.embed = embed

    async def send_to(self, recipient: Union[discord.Member, discord.TextChannel]) -> discord.Message:
        return await recipient.send(content=self.content, embed=self.embed)
