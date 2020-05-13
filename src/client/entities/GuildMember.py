from discord import Member
import utils.Logger as Log
from datetime import datetime


class GuildMember:
    def __init__(self, member: Member):
        self.member = member

    def send(self, content=None, *args, **kwargs):
        Log.info(f'{datetime.now()}, {self.member.display_name}, {self.member.id}, {content}')
        return self.member.send(content, *args, **kwargs)

    def __getattr__(self, item):
        return self.member.__getattribute__(item)
