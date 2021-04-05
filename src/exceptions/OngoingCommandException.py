from exceptions.BotException import BotException


class OngoingCommandException(BotException):
    def __init__(self):
        message = 'Another command is already running. Finish it before starting a new one.'
        super(OngoingCommandException, self).__init__(message)
