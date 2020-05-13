from exceptions.BotException import BotException


class InvalidArgumentException(BotException):
    def __init__(self, message: str):
        super(InvalidArgumentException, self).__init__(message)
