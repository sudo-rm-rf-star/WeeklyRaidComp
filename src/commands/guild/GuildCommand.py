from commands.BotCommand import BotCommand
from typing import Optional


class GuildCommand(BotCommand):
    def __init__(self, *, subname: str, description: str, argformat: Optional[str] = None):
        super(GuildCommand, self).__init__(name='guild', subname=subname, description=description, argformat=argformat)
