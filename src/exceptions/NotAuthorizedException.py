from src.exceptions.BotException import BotException


class NotAuthorizedException(BotException):
    def __init__(self, user, rank):
        super(NotAuthorizedException, self).__init__(f"User {user} not authorized. This is a {rank} command.")
