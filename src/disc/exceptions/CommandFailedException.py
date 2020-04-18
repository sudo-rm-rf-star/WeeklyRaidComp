from src.disc.exceptions import BotException


class CommandFailedException(BotException):
    def __init__(self):
        super(commandfailedexception, self).__init__("command failed to execute")
