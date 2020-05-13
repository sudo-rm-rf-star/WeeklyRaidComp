from exceptions.BotException import BotException
import discord
from client.entities.GuildMember import GuildMember


class NotAuthorizedException(BotException):
    def __init__(self, member: GuildMember, rank: str):
        super(NotAuthorizedException, self).__init__(f"User {member.display_name} not authorized. This is a {rank} command.")
