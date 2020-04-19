from src.commands.BotCommand import BotCommand
from src.common.Constants import OFFICER_RANK


class RaidInfoCommand(BotCommand):
    def __init__(self, subname, description, argformat):
        allow_trough_approval = False
        required_rank = OFFICER_RANK
        super(RaidInfoCommand, self).__init__('raidinfo', subname, description, argformat, required_rank,
                                              allow_trough_approval)
