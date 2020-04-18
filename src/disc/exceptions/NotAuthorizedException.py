from src.disc.exceptions.BotException import BotException


class NotAuthorizedException(BotException):
    def __init__(self):
        super(NotAuthorizedException, self).__init__("User not authorized")
