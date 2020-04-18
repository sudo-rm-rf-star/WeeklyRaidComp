from datetime import datetime
from src.common.Constants import DATE_FORMAT
import re


def parse_date(date):
    return datetime.strptime(date, DATE_FORMAT)


def parse_name(row):
    regex = r"[a-zA-ZöÓòéëû]+"
    matches = re.findall(regex, row)
    if not (len(matches)):
        print(f"Failed to process {row}. Please contact Groovypanda")
        exit(1)

    charname = re.findall(regex, row)[0]
    return charname.strip().capitalize()
