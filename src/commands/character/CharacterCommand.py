from commands.BotCommand import BotCommand


class CharacterCommand(BotCommand):
    def __init__(self, subname: str, description: str, argformat: str, required_rank: str = None, example_args: str = None):
        super(CharacterCommand, self).__init__('character', subname, description, argformat, required_rank, example_args)
