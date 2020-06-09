from commands.BotCommand import BotCommand
from typing import Optional


class RaidInfoCommand(BotCommand):
    def __init__(self, *, subname: str, description: str, argformat: Optional[str] = None):
        super(RaidInfoCommand, self).__init__(name='raidinfo', subname=subname, description=description, argformat=argformat)
