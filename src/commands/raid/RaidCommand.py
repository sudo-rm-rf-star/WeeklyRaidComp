from src.commands.BotCommand import BotCommand


class RaidCommand(BotCommand):
    def __init__(self, subname, description, argformat, required_rank, allow_trough_approval=False):
        super(RaidCommand, self).__init__('raid', subname, description, argformat, required_rank, allow_trough_approval)
