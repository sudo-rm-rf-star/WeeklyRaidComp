from src.disc.exceptions.BotException import BotException


class InvalidArgumentException(BotException):
    def __init__(self, message):
        super(InvalidArgumentException, self).__init__(message)
