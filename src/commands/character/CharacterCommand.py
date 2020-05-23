from commands.BotCommand import BotCommand


class PlayerCommand(BotCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str = None, example_args: str = None):
        super(PlayerCommand, self).__init__('character', subname, description, argformat, required_rank, example_args)
