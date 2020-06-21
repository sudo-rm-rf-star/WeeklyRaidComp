from client.entities.GuildMember import GuildMember
from exceptions.InternalBotException import InternalBotException
from typing import Union, Dict, Any, List, Optional
from utils.DiscordUtils import get_emoji, get_message
from utils.EmojiNames import ROLE_EMOJI, ROLE_CLASS_EMOJI, SIGNUP_STATUS_EMOJI
from logic.Character import Character
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.MessageRef import MessageRef
import json
import discord
import utils.Logger as Log

EMPTY_FIELD = '\u200e'


class DiscordMessage:
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, content: str = None, embed: discord.Embed = None):
        self.discord_client = discord_client
        self.discord_guild = discord_guild
        self.content = content
        self.embed = embed

    async def send_to(self, recipient: Union[GuildMember, discord.TextChannel]) -> List[discord.Message]:
        messages = []
        try:
            if self.embed:
                for embed in split_large_embed(self.embed.to_dict()):
                    embed = discord.Embed.from_dict(embed)
                    messages.append(await recipient.send(embed=embed))
            if self.content:
                messages.append(await recipient.send(content=self.content))
            return messages
        except discord.HTTPException as e:
            if e.code == "50035":  # Invalid Form Body
                Log.warn(f'Failed to send following message to {recipient}: content {self.content}, embed: {self.embed.to_dict()}. Splitting message')
            raise e

    def _role_emoji(self, role: Role) -> discord.Emoji:
        return self._get_emoji(ROLE_EMOJI[role])

    def _role_class_emoji(self, character: Character) -> discord.Emoji:
        return self._get_emoji(ROLE_CLASS_EMOJI[character.role][character.klass])

    def _signup_choice_emoji(self, signup_choice: SignupStatus) -> discord.Emoji:
        return self._get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return get_emoji(self.discord_guild, name)

    @staticmethod
    def _field(content: str, inline: bool = True):
        return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}

    def _empty_field(self, inline: bool = True):
        return self._field(EMPTY_FIELD, inline)

    async def _update_message(self, message_ref: MessageRef):
        message = await get_message(self.discord_guild, message_ref)
        if self.embed:
            await message.edit(embed=self.embed)
        if self.content:
            await message.edit(content=self.content)


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
