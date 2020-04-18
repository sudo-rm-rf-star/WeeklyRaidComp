from datetime import datetime
from src.common.Constants import DATETIME_FORMAT, DATE_FORMAT, TIME_FORMAT
from src.exceptions.CommandFailedException import CommandFailedException
import re


def to_datetime(x, fmt=DATETIME_FORMAT):
    return datetime.strptime(x, fmt)


def from_datetime(x, fmt=DATETIME_FORMAT):
    return x.strftime(fmt)


def to_date(x):
    return to_datetime(x, DATE_FORMAT)


def from_date(x):
    return from_datetime(x, DATE_FORMAT)


def from_time(x):
    return from_datetime(x, TIME_FORMAT)


def parse_name(row):
    regex = r"[a-zA-ZöÓòéëû]+"
    matches = re.findall(regex, row)
    if not (len(matches)):
        raise CommandFailedException(f"Could not parse username: {row}")

    charname = re.findall(regex, row)[0]
    return charname.strip().capitalize()


def today():
    return datetime.now().date()


def now():
    return datetime.now()
