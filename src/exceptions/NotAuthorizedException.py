from src.exceptions.BotException import BotException
import discord


class NotAuthorizedException(BotException):
    def __init__(self, member: discord.Member, rank: str):
        super(NotAuthorizedException, self).__init__(f"User {member.display_name} not authorized. This is a {rank} command.")
