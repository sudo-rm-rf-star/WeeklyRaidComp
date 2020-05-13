import discord
from client.DiscordClient import DiscordClient
from exceptions.NotAuthorizedException import NotAuthorizedException
from client.entities.GuildMember import GuildMember


async def delete_bot_messages(client: DiscordClient, text_channel: discord.TextChannel):
    is_me = lambda msg: msg.author == client.client.user
    await text_channel.purge(check=is_me)


def check_authority(user: GuildMember, required_rank: str) -> None:
    if required_rank and all(required_rank != role.name for role in user.roles):
        raise NotAuthorizedException(user, required_rank)
