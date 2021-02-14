from dokbot.entities.GuildMember import GuildMember
from typing import Union, List, Optional
from dokbot.DiscordUtils import get_emoji, get_message
from utils.EmojiNames import ROLE_EMOJI, ROLE_CLASS_EMOJI, SIGNUP_STATUS_EMOJI
from logic.Character import Character
from logic.enums.Role import Role
from logic.enums.SignupStatus import SignupStatus
from logic.MessageRef import MessageRef
import discord
import utils.Logger as Log
from exceptions.InvalidInputException import InvalidInputException
from typing import Dict, Tuple, List
import math

EMPTY_FIELD = '\u200e'
MAX_FIELDS = 24
MAX_CHARACTERS_PER_ROLE = 12  # Any field has a max amount of 1024 characters


class DiscordMessage:
    def __init__(self, discord_client: discord.Client, discord_guild: discord.Guild, content: str = None,
                 embed: discord.Embed = None, emojis: List[str] = None, *args, **kwargs):
        self.discord_client = discord_client
        self.discord_guild = discord_guild
        self.content = content
        self.embed = embed
        self.emojis = emojis if emojis else []

    async def send_to(self, recipient: Union[GuildMember, discord.TextChannel]) -> List[discord.Message]:
        messages = []
        if recipient is None:
            raise InvalidInputException(f'Recipient is empty.')
        try:
            if self.embed is not None:
                embed = self.embed.to_dict()
                fields = embed['fields']
                embed['fields'] = fields[:MAX_FIELDS]
                messages.append(await recipient.send(embed=discord.Embed.from_dict(embed)))
                for i in range(MAX_FIELDS, len(fields), MAX_FIELDS):
                    messages.append(
                        await recipient.send(embed=discord.Embed.from_dict({'fields': fields[i:i + MAX_FIELDS]})))
            if self.content:
                messages.append(await recipient.send(content=self.content))
        except discord.Forbidden:
            Log.error(f'Could not send message to {recipient}')
        except discord.HTTPException as e:
            if e.code == 50035:  # Invalid Form Body
                Log.warn(
                    f'Failed to send following message to {recipient}: content {self.content}, embed: {self.embed.to_dict()}')
                raise e
        for message in messages:
            for emoji in self.emojis:
                await message.add_reaction(await get_emoji(self.discord_client, emoji))
        return messages

    async def _update_message(self, message_ref: MessageRef) -> Optional[discord.Message]:
        message = await get_message(self.discord_guild, message_ref)
        if message:
            if self.embed is not None:
                await message.edit(embed=self.embed)
            if self.content is not None:
                await message.edit(content=self.content)
        return message

    @classmethod
    async def show_characters(cls, client: discord.Client, characters: List[Character]):
        fields = []
        fields.extend(await create_character_roster(client, characters, [Role.TANK, Role.HEALER]))
        fields.extend(await create_character_roster(client, characters, [Role.MELEE, Role.RANGED]))
        return fields


async def show_characters_with_role(client: discord.Client, characters: List[Character], role: Role) -> List[Dict[str, str]]:
    chars_for_role = sorted([char for char in characters if char.role == role], key=lambda char: str(char.klass))
    i = 0
    fields = []
    while i < len(chars_for_role):
        chars = chars_for_role[i:i + MAX_CHARACTERS_PER_ROLE]
        player_lines = '\n'.join([await _get_character_line(client, char) for char in chars])
        if i == 0:
            value = f'{role_emoji(client, role)} **__{role.name.capitalize()}__** ({len(chars_for_role)}):\n{player_lines}'
            fields.append(field(value, inline=True))
        else:
            value = player_lines
            fields.append(field(value, inline=True))
        i += MAX_CHARACTERS_PER_ROLE
    return fields


async def create_character_roster(client: discord.Client, characters: List[Character], roles: List[Role]):
    chars_per_role = {
        role: sorted([char for char in characters if char.role == role], key=lambda char: str(char.klass)) for role
        in roles}
    matrix = _create_character_matrix(chars_per_role, roles)
    fields = []
    for i, row in enumerate(matrix):
        for characters in row:
            if (len(characters)) > 0:
                value = '\n'.join([await _get_character_line(client, char) for char in characters])
                if i == 0:
                    role = characters[0].role
                    value = f'{await role_emoji(client, role)} **__{role.name.capitalize()}__** ({len(chars_per_role[role])}):\n{value}'
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


async def _get_character_line(client: discord.Client, character: Character) -> str:
    signup_choice = character.get_signup_status()
    signup_choice_indicator = '' if signup_choice in [SignupStatus.ACCEPT,
                                                      SignupStatus.UNDECIDED] else await signup_choice_emoji(client, signup_choice)
    return f'{await role_class_emoji(client, character)} {character.name} {signup_choice_indicator}'


def field(content: str, inline: bool = True):
    return {'name': EMPTY_FIELD, 'value': content, 'inline': inline}


def empty_field(inline: bool = True):
    return field(EMPTY_FIELD, inline)


async def role_emoji(client: discord.Client, role: Role) -> discord.Emoji:
    return await get_emoji(client, ROLE_EMOJI[role])


async def role_class_emoji(client: discord.Client, character: Character) -> discord.Emoji:
    return await get_emoji(client, ROLE_CLASS_EMOJI[character.role][character.klass])


async def signup_choice_emoji(client: discord.Client, signup_choice: SignupStatus) -> discord.Emoji:
    return await get_emoji(client, SIGNUP_STATUS_EMOJI[signup_choice])
