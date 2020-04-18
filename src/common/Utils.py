from datetime import datetime
from src.common.Constants import DATETIME_FORMAT, DATE_FORMAT, TIME_FORMAT
from src.exceptions.CommandFailedException import CommandFailedException
import re


def to_datetime(x):
    return datetime.strptime(x, DATETIME_FORMAT)


def from_datetime(x):
    return x.strftime(DATETIME_FORMAT)


def to_date(x):
    return datetime.strptime(x, DATE_FORMAT)


def from_date(x):
    return x.strftime(DATE_FORMAT)


def from_time(x):
    return x.strftime(TIME_FORMAT)


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
