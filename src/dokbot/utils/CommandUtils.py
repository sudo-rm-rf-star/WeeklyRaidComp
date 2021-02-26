import discord
from exceptions.NotAuthorizedException import NotAuthorizedException
from dokbot.entities.discord.Member import discord.Member


async def delete_bot_messages(client: discord.Client, text_channel: discord.TextChannel):
    def is_me(msg: discord.Message):
        return msg.author == client.user

    await text_channel.purge(check=is_me)


def check_authority(user: discord.Member, required_rank: str) -> None:
    if required_rank and all(required_rank != role.name for role in user.roles):
        raise NotAuthorizedException(user, required_rank)
