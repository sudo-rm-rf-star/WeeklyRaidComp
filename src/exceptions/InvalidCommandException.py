from exceptions.BotException import BotException


class InvalidCommandException(BotException):
    def __init__(self, message: str):
        super(InvalidCommandException, self).__init__(message)
