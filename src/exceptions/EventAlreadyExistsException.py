from src.exceptions.BotException import BotException
from src.time.DateOptionalTime import DateOptionalTime


class EventAlreadyExistsException(BotException):
    def __init__(self, raid_name: str, raid_datetime: DateOptionalTime):
        super(EventAlreadyExistsException, self).__init__(f"A roster already exists for raid {raid_name} on {raid_datetime}.")
