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
    return discord.utils.get(get_guild(client).members, name=user_name)
