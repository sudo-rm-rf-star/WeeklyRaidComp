from commands.BotCommand import BotCommand


class PlayerCommand(BotCommand):
    def __init__(self, *, subname: str, description: str, argformat: str = None, example_args: str = None):
        super(PlayerCommand, self).__init__(name='player', subname=subname, description=description, argformat=argformat, example_args=example_args)
