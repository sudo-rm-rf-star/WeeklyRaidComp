import discord
import src.client.Logger as Log
from typing import Union


class DiscordMessage:
    def __init__(self, content: str = None, embed: discord.Embed = None):
        self.content = content
        self.embed = embed

    async def send_to(self, recipient: Union[discord.Member, discord.TextChannel]) -> discord.Message:
        try:
            return await recipient.send(content=self.content, embed=self.embed)
        except discord.HTTPException as e:
            Log.error(f'Failed to send following message to {recipient}: content {self.content}, embed: {self.embed.to_dict()}')
            raise e


