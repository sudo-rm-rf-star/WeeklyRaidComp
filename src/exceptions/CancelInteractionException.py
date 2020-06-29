from exceptions.BotException import BotException


class CancelInteractionException(BotException):
    def __init__(self):
        super(CancelInteractionException, self).__init__("Cancelled the interaction, nothing changed :-)")
