from commands.BotCommand import BotCommand
from utils.Constants import OFFICER_RANK


class RaidInfoCommand(BotCommand):
    def __init__(self, subname, description, argformat=''):
        required_rank = OFFICER_RANK
        super(RaidInfoCommand, self).__init__('raidinfo', subname, description, argformat, required_rank)
