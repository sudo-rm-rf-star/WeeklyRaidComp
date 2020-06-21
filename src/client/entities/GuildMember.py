from discord import Member
import utils.Logger as Log
from datetime import datetime


class GuildMember:
    def __init__(self, member: Member, guild_id: int):
        self.member = member
        self.guild_id = guild_id

    def send(self, content=None, *args, **kwargs):
        Log.info(f'{datetime.now()}, {self.member.display_name}, {self.member.id}, {content}')
        return self.member.send(content, *args, **kwargs)

    def __getattr__(self, item):
        return self.member.__getattribute__(item)

    def __str__(self):
        return str(self.member)
