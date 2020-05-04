import discord
import src.client.Logger as Log
from src.exceptions.InternalBotException import InternalBotException
from typing import Union, Dict, Any, List, Optional
import json


class DiscordMessage:
    def __init__(self, content: str = None, embed: discord.Embed = None):
        self.content = content
        self.embed = embed

    async def send_to(self, recipient: Union[discord.Member, discord.TextChannel]) -> List[discord.Message]:
        messages = []
        try:
            for embed in split_large_embed(self.embed.to_dict()):
                embed = discord.Embed.from_dict(embed)
                messages.append(await recipient.send(embed=embed))
            if self.content:
                messages.append(await recipient.send(content=self.content))
            return messages
        except discord.HTTPException as e:
            if e.response == "Bad Request":  # Invalid Form Body
                Log.warn(f'Failed to send following message to {recipient}: content {self.content}, embed: {self.embed.to_dict()}. Splitting message')
            raise e


def split_large_embed(embed: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """
    Fix embed to stay within Discord API limits: https://discordapp.com/developers/docs/resources/channel#embed-limits
    TODO: we don't take into account everything yet, but issues can be fixed here as needed.
    title	256 characters
    description	2048 characters
    fields	Up to 25 field objects
    field.name	256 characters
    field.value	1024 characters
    footer.text	2048 characters
    author.name	256 characters
    """
    if embed is None:
        return None

    limit_length = 6000
    head_embed = embed
    tail_embed = embed

    fields = embed['fields']
    field_count = len(embed['fields'])
    embed_length = len(json.dumps(head_embed))

    while embed_length > limit_length and field_count > 0:
        field_count -= 1
        head_embed['fields'] = fields[:field_count]
        embed_length = len(json.dumps(head_embed))
    if embed_length > limit_length and field_count == 0:
        raise InternalBotException(f"Reached max recursive depth with embed: {embed}")
    if field_count == len(embed['fields']):
        return [head_embed]

    tail_embed['fields'] = fields[field_count:]
    embeds = [head_embed]
    embeds.extend(split_large_embed(tail_embed))
    return embeds
