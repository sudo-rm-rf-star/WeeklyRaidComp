from exceptions.BotException import BotException


class InvalidInputException(BotException):
    def __init__(self, message: str):
        super(InvalidInputException, self).__init__(message)
