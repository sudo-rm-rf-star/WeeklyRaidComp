from exceptions.BotException import BotException


class InternalBotException(BotException):
    def __init__(self, message: str):
        super(InternalBotException, self).__init__(message)
