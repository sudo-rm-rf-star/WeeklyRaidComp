from src.exceptions.BotException import BotException


class InvalidCommandException(BotException):
    def __init__(self, message):
        super(InvalidCommandException, self).__init__(message)
