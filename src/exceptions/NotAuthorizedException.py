from dokbot.entities.discord.Member import discord.Member
from exceptions.BotException import BotException


class NotAuthorizedException(BotException):
    def __init__(self, member: discord.Member, rank: str):
        super(NotAuthorizedException, self).__init__(f"User {member.display_name} not authorized. This is a {rank} command.")
