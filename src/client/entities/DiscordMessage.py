from client.entities.GuildMember import GuildMember
from typing import Union, List, Optional
from utils.DiscordUtils import get_emoji, get_message
from utils.EmojiNames import ROLE_EMOJI, ROLE_CLASS_EMOJI, SIGNUP_STATUS_EMOJI
from logic.Character import Character
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.MessageRef import MessageRef
import discord
import utils.Logger as Log
from exceptions.InvalidArgumentException import InvalidArgumentException
import math

EMPTY_FIELD = '\u200e'
MAX_FIELDS = 12


class DiscordMessage:
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, content: str = None,
                 embed: discord.Embed = None):
        self.discord_client = discord_client
        self.discord_guild = discord_guild
        self.content = content
        self.embed = embed

    async def send_to(self, recipient: Union[GuildMember, discord.TextChannel]) -> List[discord.Message]:
        messages = []
        if recipient is None:
            raise InvalidArgumentException(f'Recipient is empty.')
        try:
            if self.embed:
                embed = self.embed.to_dict()
                fields = embed['fields']
                embed['fields'] = fields[:MAX_FIELDS]
                messages.append(await recipient.send(embed=discord.Embed.from_dict(embed)))
                for i in range(MAX_FIELDS, len(fields), MAX_FIELDS):
                    messages.append(
                        await recipient.send(embed=discord.Embed.from_dict({'fields': fields[i:i + MAX_FIELDS]})))
            if self.content:
                messages.append(await recipient.send(content=self.content))
        except discord.Forbidden as e:
            Log.error(f'Could not send message to {recipient}')
        except discord.HTTPException as e:
            if e.code == 50035:  # Invalid Form Body
                Log.warn(
                    f'Failed to send following message to {recipient}: content {self.content}, embed: {self.embed.to_dict()}. \nSplitting message')
        return messages

    def _role_emoji(self, role: Role) -> discord.Emoji:
        return self._get_emoji(ROLE_EMOJI[role])

    def _role_class_emoji(self, character: Character) -> discord.Emoji:
        return self._get_emoji(ROLE_CLASS_EMOJI[character.role][character.klass])

    def _signup_choice_emoji(self, signup_choice: SignupStatus) -> discord.Emoji:
        return self._get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])

    def _get_emoji(self, name: str) -> discord.Emoji:
        return get_emoji(self.discord_guild, name)

    def split_column_evenly(self, lines: List[str], column_count: int = 3, column_width=3):
        assert column_width <= 3
        fields = []
        if len(lines) <= 2 * column_count:
            fields.append(self._field("\n".join(lines), inline=True))
            fields.append(self._empty_field(inline=True))
            fields.append(self._empty_field(inline=True))
        else:
            values_per_col = math.ceil(len(lines) / column_count)
            current_width = 0
            for i in range(0, len(lines), values_per_col):
                column_lines = lines[i:i + values_per_col]
                fields.append(self._field("\n".join(column_lines), inline=True))
                current_width += 1
        return fields

    @staticmethod
    def _field(content: str, inline: bool = True):
        return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}

    def _empty_field(self, inline: bool = True):
        return self._field(EMPTY_FIELD, inline)

    async def _update_message(self, message_ref: MessageRef) -> Optional[discord.Message]:
        message = await get_message(self.discord_guild, message_ref)
        if message:
            if self.embed:
                await message.edit(embed=self.embed)
            if self.content:
                await message.edit(content=self.content)
        return message


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
