from src.exceptions.BotException import BotException


class CommandFailedException(BotException):
    def __init__(self, message: str):
        super(CommandFailedException, self).__init__(message)
