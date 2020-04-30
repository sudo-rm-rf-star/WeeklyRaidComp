from src.exceptions.InvalidArgumentException import InvalidArgumentException
from src.time.Time import Time
from src.time.Date import Date
from datetime import datetime

""" Wrapper over date and datetime for which time can be empty. """


class DateOptionalTime:
    def __init__(self, date: Date, time: Time = None):
        if date is None:
            raise InvalidArgumentException('No date was passed')
        assert isinstance(date, Date)
        assert isinstance(time, Time)
        self.time = time
        self.date = date

    def to_datetime(self):
        time = datetime.min.time() if not self.time else self.time.time
        return datetime.combine(self.date.date, time)

    def weekday(self):
        return self.date.weekday()

    @staticmethod
    def now():
        return DateOptionalTime(Date.now(), Time.now())

    @staticmethod
    def from_datetime(datetime_obj):
        return DateOptionalTime(datetime_obj.date(), datetime_obj.time())

    @staticmethod
    def from_string(datetime_str):
        datetime_strs = datetime_str.split(' ')
        if len(datetime_str.strip()) == 0:
            raise InvalidArgumentException('No date was passed')
        if len(datetime_str > 2):
            raise InvalidArgumentException(f'Invalid datetime was passed. Please format your date as {DateOptionalTime.now()} or {Date.now()}')
        time = Time(datetime_strs[1]) if len(datetime_strs == 2) else None
        date = Date(datetime_strs[0])
        return DateOptionalTime(date, time)

    def __eq__(self, other):
        assert isinstance(other, DateOptionalTime)
        eq = other.date == self.date
        if other.time and self.time:
            eq = eq and other.time == self.time
        return eq

    def __hash__(self):
        return hash((self.date, self.time))

    def __lt__(self, other):
        assert isinstance(other, DateOptionalTime)
        lt = self.date < other.date
        if other.time and self.time:
            lt = lt and other.time < self.time
        return lt

    def __ge__(self, other):
        assert isinstance(other, DateOptionalTime)
        return not self < other

    def __str__(self):
        strr = str(self.date)
        strr += ' ' + str(self.time) if self.time else ''
        return strr
