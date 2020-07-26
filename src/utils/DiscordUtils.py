from typing import List
from exceptions.MissingImplementationException import MissingImplementationException

import discord

from logic.MessageRef import MessageRef
from client.entities.GuildMember import GuildMember
from exceptions.InternalBotException import InternalBotException
from typing import Optional


def get_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel:
    return discord.utils.get(guild.text_channels, name=channel_name)


async def get_channels(guild: discord.Guild) -> List[discord.TextChannel]:
    if len(guild.channels) > 0:
        return guild.channels
    return await guild.fetch_channels()


def get_channels_non_async(guild: discord.Guild) -> List[discord.TextChannel]:
    return guild.channels


async def get_channel_by_id(guild: discord.Guild, channel_id: int) -> discord.TextChannel:
    channels = await guild.fetch_channels() if not get_channels_non_async(guild) else get_channels_non_async(guild)
    return discord.utils.get(channels, id=channel_id)


def get_emoji(guild: discord.Guild, emoji_name: str) -> discord.Emoji:
    return discord.utils.get(guild.emojis, name=emoji_name)


def get_member(guild: discord.Guild, user_name: str) -> Optional[GuildMember]:
    member = guild.get_member_named(user_name)
    if member is None:
        return None
    return GuildMember(member, guild.id)


async def get_member_by_id(guild: discord.Guild, user_id: int) -> GuildMember:
    member = await guild.fetch_member(user_id)
    return GuildMember(member, guild.id)


def get_users(guild: discord.Guild) -> List[GuildMember]:
    return [GuildMember(member, guild.id) for member in guild.members]


async def get_role(guild: discord.Guild, role_name: str) -> discord.Role:
    roles = await get_roles(guild)
    return discord.utils.get(roles, name=role_name)


async def get_roles(guild: discord.Guild) -> List[discord.Role]:
    return await guild.fetch_roles()


def get_roles_non_async(guild: discord.Guild) -> List[discord.Role]:
    return guild.roles


async def get_members_for_role(guild: discord.Guild, role_name: str) -> List[GuildMember]:
    role = await get_role(guild, role_name)
    return [GuildMember(member, guild.id) for member in role.members]


async def get_message(guild: discord.Guild, message_ref: MessageRef) -> discord.Message:
    if message_ref.channel_id:
        text_channel = await get_channel_by_id(guild, message_ref.channel_id)
        try:
            return await text_channel.fetch_message(message_ref.message_id)
        except discord.NotFound:
            raise InternalBotException("Could not find message")
    else:
        raise MissingImplementationException()
