import re
import requests
from datetime import timedelta
from collections import defaultdict
from src.logic.Raid import Raid
from src.common.Constants import USE_SIGNUP_HISTORY
from src.common.Utils import now
from datetime import datetime
from logging import getLogger


# https://classic.warcraftlogs.com/guild/attendance/510080
zoneId = {
    'zg': 1003,
    'bwl': 1002,
    'mc': 1000
}


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_raid_attendance_html(raid):
    return requests.get(f'https://classic.warcraftlogs.com/guild/attendance-table/510080/0/{zoneId[raid]}').text


hdr_rex = r'var createdDate = new Date\(([0-9]*)\)'
row_rex = r'<tr><td[^>]*>([a-zA-ZöÓòéëû]*)'
col_rex = '(present|absent)'


def get_raid_attendance_history(raid):
    if raid not in zoneId:
        getLogger().warning(f"There's no history yet for {raid.upper()}")
        return {}, {}

    raid_attendance_html = get_raid_attendance_html(raid)
    dates = list(
        map(lambda x: datetime.fromtimestamp(float(x) / 1000).date(), re.findall(hdr_rex, raid_attendance_html)))
    charnames = re.findall(row_rex, raid_attendance_html)
    was_present = list(map(lambda x: x == 'present', re.findall(col_rex, raid_attendance_html)))
    raid_presence = defaultdict(set)
    raid_absence = defaultdict(set)
    for charname, presence in zip(charnames, chunks(was_present, len(dates))):
        for date, present in zip(dates, presence):
            if present:
                raid_presence[charname].add(date)
            else:
                raid_absence[charname].add(date)
    return raid_presence, raid_absence


def get_raid_signup_history(raid_name):
    signup_history = defaultdict(set)
    for raid in Raid.load_all():
        if raid_name == raid.name and raid.datetime < now():
            for signee in raid.signees():
                signup_history[signee['name']].add(raid.datetime)
    return signup_history


def get_standby_count(raid, raid_datetime, week_count_cutoff=12):
    signup_history = get_raid_signup_history(raid)
    presence_history, absence_history = get_raid_attendance_history(raid)
    standby_count = {}
    all_chars = set(signup_history.keys()).union(set(presence_history.keys()))
    history_cutoff = raid_datetime - timedelta(days=week_count_cutoff * 7)

    for charname in all_chars:
        if USE_SIGNUP_HISTORY:
            # A character counts for standby if he signed up for the raid and he was not present in the raid.
            standby_dates = signup_history[charname].difference(presence_history[charname])
        else:
            # A character counts for standby if he was not present in the raid
            standby_dates = absence_history[charname]

        standby_count[charname] = len({date for date in standby_dates if date > history_cutoff})

    return standby_count
