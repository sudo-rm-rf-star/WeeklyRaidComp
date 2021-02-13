from typing import List
from typing import Optional

import discord
from dokbot.entities.GuildMember import GuildMember
from exceptions.InternalBotException import InternalBotException
from exceptions.MissingImplementationException import MissingImplementationException
from logic.Character import Character
from logic.MessageRef import MessageRef
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from utils.Constants import BASE_GUILD_ID


async def get_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel:
    channels = await get_channels(guild)
    return discord.utils.get(channels, name=channel_name)


async def create_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel:
    return await guild.create_text_channel(channel_name)


async def get_channels(guild: discord.Guild) -> List[discord.TextChannel]:
    if len(guild.text_channels) > 0:
        return guild.text_channels
    return await guild.fetch_channels()


async def get_channel_by_id(guild: discord.Guild, channel_id: int) -> discord.TextChannel:
    channels = await get_channels(guild)
    return discord.utils.get(channels, id=channel_id)


async def get_emoji(client: discord.Client, emoji_name: str) -> discord.Emoji:
    emoji = discord.utils.get(client.emojis, name=emoji_name)
    if emoji is None:
        base_guild: discord.Guild = await client.fetch_guild(BASE_GUILD_ID)
        file_name = f"static/emojis/{emoji_name}.png"
        try:
            with open(file_name, "rb") as image:
                return await base_guild.create_custom_emoji(name=emoji_name, image=image.read())
        except FileNotFoundError:
            raise InternalBotException(f'Could not find {file_name}')


    return emoji


async def get_member(guild: discord.Guild, user_name: str) -> Optional[GuildMember]:
    async for member in guild.fetch_members(limit=None):
        if member.display_name == user_name or member.name == user_name:
            return member
    return None


async def get_member_by_id(guild: discord.Guild, user_id: int) -> GuildMember:
    member = await guild.fetch_member(user_id)
    return GuildMember(member, guild.id)


async def get_role(guild: discord.Guild, role_name: str) -> discord.Role:
    roles = await get_roles(guild)
    return discord.utils.get(roles, name=role_name)


async def get_roles(guild: discord.Guild) -> List[discord.Role]:
    return await guild.fetch_roles() if len(guild.roles) == 0 else guild.roles


def get_roles_non_async(guild: discord.Guild) -> List[discord.Role]:
    return guild.roles


def get_channels_non_async(guild: discord.Guild) -> List[discord.TextChannel]:
    return guild.text_channels


async def get_members_for_role(guild: discord.Guild, role_name: str) -> List[GuildMember]:
    role = await get_role(guild, role_name)
    return [GuildMember(member, guild.id) for member in role.members]


async def get_message(guild: discord.Guild, message_ref: MessageRef) -> Optional[discord.Message]:
    if message_ref.channel_id:
        text_channel = await get_channel_by_id(guild, message_ref.channel_id)
        try:
            return await text_channel.fetch_message(message_ref.message_id)
        except discord.NotFound:
            return None
    else:
        raise MissingImplementationException()


async def set_roster_status(guild: discord.Guild, member: GuildMember, character: Character):
    roster_status = character.get_roster_status()
    signup_status = character.get_signup_status()
    roster_role = await get_role(guild, "Roster")
    roster_roles = {status: await _roster_status_to_role(guild, status) for status in list(RosterStatus)}
    remove_roles = list(roster_roles.values())
    add_roles = [roster_roles[roster_status]]
    if roster_status in [RosterStatus.ACCEPT, RosterStatus.EXTRA] and signup_status != SignupStatus.DECLINE:
        add_roles.append(roster_role)
    else:
        remove_roles.append(roster_role)
    await member.member.remove_roles(*remove_roles)
    await member.member.add_roles(*add_roles)


async def _roster_status_to_role(guild: discord.Guild, roster_status: RosterStatus) -> discord.Role:
    role_name = f'Roster{str(roster_status.name).capitalize()}'
    role = await get_role(guild, role_name)
    if not role:
        role = await guild.create_role(name=role_name)
    return role
