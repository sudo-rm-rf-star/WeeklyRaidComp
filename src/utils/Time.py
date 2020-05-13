from exceptions.InvalidArgumentException import InvalidArgumentException
from utils.Constants import TIME_FORMAT
import datetime


class Time:
    def __init__(self, time: datetime.time):
        self.time = time

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return self.time.strftime(TIME_FORMAT)

    def __hash__(self):
        return hash(self.time)

    @staticmethod
    def from_string(time_str):
        try:
            return Time(datetime.datetime.strptime(time_str, TIME_FORMAT).time())
        except ValueError:
            raise InvalidArgumentException(f"Invalid time. Please format time as {str(Time.now())}")

    @staticmethod
    def now():
        return Time(datetime.datetime.now().time())
