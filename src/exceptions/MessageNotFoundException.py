from exceptions.BotException import BotException


class MessageNotFoundException(BotException):
    def __init__(self, message: str):
        super(MessageNotFoundException, self).__init__(message)
