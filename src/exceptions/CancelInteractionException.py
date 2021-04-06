from exceptions.BotException import BotException


class CancelInteractionException(BotException):
    def __init__(self, message: str):
        super(CancelInteractionException, self).__init__(message)
