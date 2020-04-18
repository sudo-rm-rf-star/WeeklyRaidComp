import discord
from src.common.Constants import GUILD, BOT_NAME


def get_guild(client):
    return discord.utils.get(client.guilds, name=GUILD)


def get_bot(client, bot_name=BOT_NAME):
    return discord.utils.get(get_guild(client).members, name=bot_name)


def get_channel(client, channel_name):
    return discord.utils.get(get_guild(client).channels, name=channel_name)


def get_emoji(client, emoji_name):
    return discord.utils.get(get_guild(client).emojis, name=emoji_name)


def get_user(client, user_name):
    return get_guild(client).get_member_named(user_name)


def get_user_by_id(client, user_id):
    return get_guild(client).get_member(user_id)


def get_users(client):
    return get_guild(client).members


def get_role(client, role_name):
    return discord.utils.get(get_guild(client).roles, name=role_name)


def get_members_for_role(client, role_name):
    return get_role(client, role_name).members
