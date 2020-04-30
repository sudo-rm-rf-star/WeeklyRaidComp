from src.exceptions.BotException import BotException


class EventDoesNotExistException(BotException):
    def __init__(self, message: str):
        super(EventDoesNotExistException, self).__init__(message)
