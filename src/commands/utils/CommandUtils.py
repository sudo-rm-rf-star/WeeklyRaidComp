import discord
from src.client.GuildClient import GuildClient
from src.exceptions.NotAuthorizedException import NotAuthorizedException
from typing import Union


async def delete_bot_messages(client: GuildClient, text_channel: discord.TextChannel):
    is_me = lambda msg: msg.author == client.client.user
    await text_channel.purge(check=is_me)


def check_authority(server: GuildClient, user: Union[discord.User, discord.Member], required_rank: str) -> None:
    if isinstance(user, discord.User):
        user = server.get_member_by_id(user.id)
    if required_rank and all(required_rank != role.name for role in user.roles):
        raise NotAuthorizedException(user, required_rank)
