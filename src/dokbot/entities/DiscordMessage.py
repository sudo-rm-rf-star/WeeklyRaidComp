from exceptions.InternalBotException import InternalBotException
from typing import Optional
from dokbot.utils.DiscordUtils import get_message
from utils.EmojiNames import ROLE_EMOJI, ROLE_CLASS_EMOJI
from logic.Character import Character
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.MessageRef import MessageRef
import discord
from dokbot.DokBotContext import DokBotContext
import utils.Logger as Log
from exceptions.InvalidInputException import InvalidInputException
from typing import Dict, List
import math
import asyncio

EMPTY_FIELD = '\u200e'
MAX_FIELDS = 24
MAX_CHARACTERS_PER_ROLE = 12  # Any field has a max amount of 1024 characters


class DiscordMessage:
    def __init__(self, ctx: DokBotContext,
                 content: str = None,
                 embed: discord.Embed = None,
                 reactions: List[str] = None,
                 **kwargs):
        self.ctx = ctx
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.content = content
        self.embed = embed
        self.emojis = reactions if reactions else []

    @classmethod
    async def get_embed(cls, ctx: DokBotContext, **kwargs) -> Optional[discord.Embed]:
        return None

    @classmethod
    async def make(cls, ctx: DokBotContext, **kwargs):
        embed = await cls.get_embed(ctx, **kwargs)
        return cls(ctx=ctx, embed=embed, **kwargs)

    @classmethod
    async def send(cls, ctx: DokBotContext, recipient, **kwargs):
        discord_message = await cls.make(ctx=ctx, **kwargs)
        if discord_message:
            return await discord_message.send_to(recipient)

    @classmethod
    async def reply_to_author(cls, ctx: DokBotContext, **kwargs):
        return await cls.send(ctx=ctx, recipient=ctx.author, **kwargs)

    @classmethod
    async def reply_in_channel(cls, ctx: DokBotContext, **kwargs):
        return await cls.send(ctx=ctx, recipient=ctx.channel, **kwargs)

    async def send_to(self, recipient) -> List[discord.Message]:
        messages = []
        if recipient is None:
            raise InvalidInputException(f'Recipient is empty.')
        try:
            if self.embed:
                embed = self.embed.to_dict()
                fields = embed.get('fields', [])
                embed['fields'] = fields[:MAX_FIELDS]
                messages.append(await recipient.send(embed=discord.Embed.from_dict(embed)))
                for i in range(MAX_FIELDS, len(fields), MAX_FIELDS):
                    messages.append(
                        await recipient.send(embed=discord.Embed.from_dict({'fields': fields[i:i + MAX_FIELDS]})))
            elif self.content:
                messages.append(await recipient.send(content=self.content))
            else:
                raise InternalBotException('You need to set either embed or content.')
        except discord.Forbidden:
            Log.error(f'Could not send message to {recipient}')
        except discord.HTTPException as e:
            if e.code == 50035:  # Invalid Form Body
                Log.warn(
                    f'Failed to send following message to {recipient}: content {self.content}, embed: {self.embed.to_dict()}')
                raise e
        asyncio.create_task(self.add_emojis(messages))
        return messages

    async def add_emojis(self, messages):
        for message in messages:
            current_emojis = set([reaction.emoji.name for reaction in message.reactions])
            for emoji in self.emojis:
                if emoji not in current_emojis:
                    await message.add_reaction(await self.ctx.bot.emoji(emoji))

    async def update_by_ref(self, message_ref: MessageRef) -> Optional[discord.Message]:
        message = await get_message(self.ctx.guild, message_ref)
        return await self.update(message)

    async def update(self, discord_message: discord.Message) -> Optional[discord.Message]:
        if discord_message:
            if self.embed is not None:
                await discord_message.edit(embed=self.embed)
            if self.content is not None:
                await discord_message.edit(content=self.content)
            asyncio.create_task(self.add_emojis([discord_message]))
        return discord_message

    @classmethod
    async def show_characters(cls, ctx: DokBotContext, characters: List[Character]):
        fields = []
        fields.extend(await create_character_roster(ctx, characters, [Role.TANK, Role.HEALER]))
        fields.extend(await create_character_roster(ctx, characters, [Role.MELEE, Role.RANGED]))
        return fields


async def show_characters_with_role(ctx: DokBotContext, characters: List[Character], role: Role) -> List[Dict[str, str]]:
    chars_for_role = sorted([char for char in characters if char.role == role], key=lambda char: str(char.klass))
    i = 0
    fields = []
    while i < len(chars_for_role):
        chars = chars_for_role[i:i + MAX_CHARACTERS_PER_ROLE]
        player_lines = '\n'.join([await _get_character_line(ctx, char) for char in chars])
        if i == 0:
            value = f'{role_emoji(ctx, role)} **__{role.name.capitalize()}__** ({len(chars_for_role)}):\n{player_lines}'
            fields.append(field(value, inline=True))
        else:
            value = player_lines
            fields.append(field(value, inline=True))
        i += MAX_CHARACTERS_PER_ROLE
    return fields


async def create_character_roster(ctx: DokBotContext, characters: List[Character], roles: List[Role]):
    chars_per_role = {
        role: sorted([char for char in characters if char.role == role], key=lambda char: str(char.klass)) for role
        in roles}
    matrix = _create_character_matrix(chars_per_role, roles)
    fields = []
    for i, row in enumerate(matrix):
        for characters in row:
            if (len(characters)) > 0:
                value = '\n'.join([await _get_character_line(ctx, char) for char in characters])
                if i == 0:
                    role = characters[0].role
                    value = f'{await role_emoji(ctx, role)} **__{role.name.capitalize()}__** ({len(chars_per_role[role])}):\n{value}'
                fields.append(field(value, inline=True))
            else:
                fields.append(empty_field())
        fields.append(empty_field())
    return fields


# Create a nx3 roster where every column is a role with max 12 characters.If there are more, new rows are added.
def _create_character_matrix(chars_per_role: Dict[Role, List[Character]], roles: List[Role]):
    n_rows = math.ceil(max([len(chars) for chars in chars_per_role.values()]) / MAX_CHARACTERS_PER_ROLE)
    n_cols = len(roles)
    roster = [[[] for _ in range(n_cols)] for _ in range(n_rows)]
    for i_row in range(n_rows):
        for (i_col, role) in enumerate(roles):
            i_character = sum(len(row[i_col]) for row in roster)
            roster[i_row][i_col] = chars_per_role[role][i_character:i_character + MAX_CHARACTERS_PER_ROLE]
    return roster


async def _get_character_line(ctx: DokBotContext, character: Character) -> str:
    signup_choice = character.get_signup_status()
    signup_choice_indicator = '' if signup_choice in [SignupStatus.Accept, SignupStatus.Unknown] else await ctx.bot.emoji(signup_choice.name)
    return f'{await role_class_emoji(ctx, character)} {character.name} {signup_choice_indicator}'


def field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def empty_field(inline: bool = True):
    return field(EMPTY_FIELD, inline)


async def role_emoji(ctx: DokBotContext, role: Role) -> discord.Emoji:
    return await ctx.bot.emoji(ROLE_EMOJI[role])


async def role_class_emoji(ctx: DokBotContext, character: Character) -> discord.Emoji:
    return await ctx.bot.emoji(ROLE_CLASS_EMOJI[character.role][character.klass])
