from commands.BotCommand import BotCommand


class RaidCommand(BotCommand):
    def __init__(self, *, subname, description, argformat):
        super(RaidCommand, self).__init__(name='raid', subname=subname, description=description, argformat=argformat)
