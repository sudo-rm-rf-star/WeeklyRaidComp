from commands.BotCommand import BotCommand


class GuildCommand(BotCommand):
    def __init__(self, subname, description, argformat, required_rank):
        super(GuildCommand, self).__init__('guild', subname, description, argformat, required_rank)
