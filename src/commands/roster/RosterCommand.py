from src.commands.BotCommand import BotCommand


class RosterCommand(BotCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str, allow_trough_approval: bool = False):
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank, allow_trough_approval)
