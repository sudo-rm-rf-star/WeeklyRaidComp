from typing import List
from typing import Optional

import discord

from client.entities.GuildMember import GuildMember
from exceptions.InternalBotException import InternalBotException
from exceptions.MissingImplementationException import MissingImplementationException
from logic.Character import Character
from logic.MessageRef import MessageRef
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus


async def get_channel(guild: discord.Guild, channel_name: str) -> discord.TextChannel:
    channels = await get_channels(guild)
    return discord.utils.get(channels, name=channel_name)


async def get_channels(guild: discord.Guild) -> List[discord.TextChannel]:
    if len(guild.text_channels) > 0:
        return guild.text_channels
    return await guild.fetch_channels()


async def get_channel_by_id(guild: discord.Guild, channel_id: int) -> discord.TextChannel:
    channels = await get_channels(guild)
    return discord.utils.get(channels, id=channel_id)


def get_emoji(client: discord.Client, emoji_name: str) -> discord.Emoji:
    emoji = discord.utils.get(client.emojis, name=emoji_name)
    if emoji is None:
        raise InternalBotException(f'{emoji_name} does not exist.')
    return emoji


def get_member(guild: discord.Guild, user_name: str) -> Optional[GuildMember]:
    member = guild.get_member_named(user_name)
    return GuildMember(member, guild.id) if member else None


async def get_member_by_id(guild: discord.Guild, user_id: int) -> GuildMember:
    member = await guild.fetch_member(user_id)
    return GuildMember(member, guild.id)


def get_users(guild: discord.Guild) -> List[GuildMember]:
    return [GuildMember(member, guild.id) for member in guild.members]


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
    roster_status = character.roster_status
    signup_status = character.signup_status
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
    return await get_role(guild, role_name)
