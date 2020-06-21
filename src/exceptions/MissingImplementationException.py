from exceptions.InternalBotException import InternalBotException


class MissingImplementationException(InternalBotException):
    def __init__(self, cls=None):
        super(MissingImplementationException, self).__init__(f"Missing implementation for {cls}")
