from commands.BotCommand import BotCommand


class RaidGroupCommand(BotCommand):
    def __init__(self, subname, description, argformat, required_rank):
        super(RaidGroupCommand, self).__init__('group', subname, description, argformat, required_rank)
