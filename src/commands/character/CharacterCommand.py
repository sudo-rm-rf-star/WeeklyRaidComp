from commands.BotCommand import BotCommand
from typing import Optional


class CharacterCommand(BotCommand):
    def __init__(self, *, subname: str, description: str, argformat: Optional[str] = None, example_args: Optional[str] = None):
        super(CharacterCommand, self).__init__(name='character', subname=subname, description=description, argformat=argformat, example_args=example_args)
