import re
from datetime import datetime
from src.logic.Constant import parse_mapping
import os
import json

kruisvaarders_filename = 'data/kruisvaarders.txt'
raid_dir = 'data/raids/input'
statuses = ['Accepted', 'Declined', 'Tentative']


def read_raids():
    raids = []
    for filename in os.listdir(raid_dir):
        with open(os.path.join(raid_dir, filename), encoding='utf-8') as signups_file:
            signups_raw = signups_file.read()
            raids.append(parse_raid(signups_raw))
    return raids


def read_raid(filename):
    with open(filename, encoding='utf-8') as signups_file:
        signups_raw = signups_file.readlines()
        return parse_raid(signups_raw)


def get_kruisvaarders():
    with open(kruisvaarders_filename, encoding='utf-8') as kruisvaarders_file:
        return [x.strip() for x in kruisvaarders_file.readlines()]


def parse_raid(blob):
    signups = []
    kruisvaarders = get_kruisvaarders()
    raid = json.loads(blob)
    raid_name = raid['name']
    dd, mm, yyyy = tuple(map(int, raid['date'].split('-')))
    raid_date = datetime(yyyy, mm, dd).date()
    for signup_state, chars in raid['signees'].items():
        for char in chars:
            charname = _get_charname(char)
            if signup_state not in ['Bench', 'Late', 'Absence', 'Tentative']:
                role, clazz = parse_mapping.get(signup_state, ('dps', signup_state.lower()))
                signups.append({'name': charname, 'class': clazz, 'role': role, 'signup_status': 'Accepted',
                                'is_kruisvaarder': charname in kruisvaarders})
            else:
                signups.append({'name': charname, 'signup_status': signup_state,
                                'is_kruisvaarder': charname in kruisvaarders})

    return raid_name, raid_date, signups


def _read_status(row):
    for status in statuses:
        if status in row:
            return status
    return None


def _get_charname(row):
    regex = r"[a-zA-ZöÓòéëû]+"
    matches = re.findall(regex, row)
    if not (len(matches)):
        print(f"Failed to process {row}. Please contact Groovypanda")
        exit(1)

    charname = re.findall(regex, row)[0]
    return charname.strip().capitalize()
