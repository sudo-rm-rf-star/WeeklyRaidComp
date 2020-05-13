from exceptions.InvalidArgumentException import InvalidArgumentException
from utils.Constants import DATE_FORMAT, WEEKDAYS
import datetime


class Date:
    def __init__(self, date: datetime.date):
        self.date = date

    def weekday(self):
        return WEEKDAYS[self.date.weekday()]

    @staticmethod
    def from_string(date_str):
        try:
            return Date(datetime.datetime.strptime(date_str, DATE_FORMAT).date())
        except ValueError:
            raise InvalidArgumentException(f"Invalid date {date_str}. Please format time as {str(Date.now())}")

    @staticmethod
    def now():
        return Date(datetime.datetime.now().date())

    def __eq__(self, other):
        assert isinstance(other, Date)
        return self.date == other.date

    def __lt__(self, other):
        assert isinstance(other, Date)
        return self.date < other.date

    def __str__(self):
        return self.date.strftime(DATE_FORMAT)

    def __hash__(self):
        return hash(self.date)

