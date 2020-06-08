import discord
from client.PlayersResource import PlayersResource
from client.entities.GuildMember import GuildMember
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier
from exceptions.InternalBotException import InternalBotException
from typing import List


def get_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel:
    return discord.utils.get(guild.text_channels, name=channel_name)


async def get_channel_by_id(guild: discord.Guild, channel_id: int) -> discord.TextChannel:
    return discord.utils.get(guild.text_channels, id=channel_id)


def get_emoji(guild: discord.Guild, emoji_name: str) -> discord.Emoji:
    return discord.utils.get(guild.emojis, name=emoji_name)


def get_member(guild: discord.Guild, user_name: str) -> GuildMember:
    return GuildMember(guild.get_member_named(user_name), guild.id)


def get_member_by_id(guild: discord.Guild, user_id: int) -> GuildMember:
    return GuildMember(guild.get_member(user_id), guild.id)


def get_users(guild: discord.Guild) -> List[GuildMember]:
    return [GuildMember(member, guild.id) for member in guild.members]


def get_role(guild: discord.Guild, role_name: str) -> discord.Role:
    return discord.utils.get(guild.roles, name=role_name)


def get_roles(guild: discord.Guild) -> List[discord.Role]:
    return guild.roles


def get_members_for_role(guild: discord.Guild, role_name: str) -> List[GuildMember]:
    return [GuildMember(member, guild.id) for member in get_role(guild, role_name).members]


async def get_message(guild: discord.Guild, message_id: DiscordMessageIdentifier) -> discord.Message:
    text_channel = await get_channel_by_id(guild, message_id.channel_id)
    try:
        return await text_channel.fetch_message(message_id.message_id)
    except discord.NotFound:
        raise InternalBotException("Could not find message")
