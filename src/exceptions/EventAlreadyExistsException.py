from src.exceptions.BotException import BotException
from src.common.Utils import from_datetime


class EventAlreadyExistsException(BotException):
    def __init__(self, raid_name, raid_datetime):
        super(EventAlreadyExistsException, self).__init__(f"A roster already exists for raid {raid_name} on {from_datetime(raid_datetime)}.")
