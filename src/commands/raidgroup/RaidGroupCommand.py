from commands.BotCommand import BotCommand
from typing import Optional


class RaidGroupCommand(BotCommand):
    def __init__(self, *, subname: str, description: str, argformat: Optional[str] = None):
        super(RaidGroupCommand, self).__init__(name='group', subname=subname, description=description, argformat=argformat)
