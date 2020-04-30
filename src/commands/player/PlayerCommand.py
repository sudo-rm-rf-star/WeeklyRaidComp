from src.commands.BotCommand import BotCommand


class PlayerCommand(BotCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str = None, allow_trough_approval: bool = False, example_args: str = None):
        super(PlayerCommand, self).__init__('player', subname, description, argformat, required_rank, allow_trough_approval, example_args)
