from src.exceptions.BotException import BotException


class InternalBotException(BotException):
    def __init__(self, message):
        super(InternalBotException, self).__init__(message)
