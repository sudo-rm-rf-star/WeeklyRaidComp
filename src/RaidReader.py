import re
from datetime import datetime
import os

kruisvaarders_filename = 'data/kruisvaarders.txt'
raid_dir = 'data/raids/input'
statuses = ['Accepted', 'Declined', 'Tentative']

parse_mapping = {
    'Tank': ('tank', 'warrior'),
    'HolyPaladin': ('healer', 'paladin'),
    'ProtPaladin': ('tank', 'paladin'),
    'Retri': ('dps', 'paladin'),
    'RestoDruid': ('healer', 'druid'),
    'Priest': ('healer', 'priest'),
    'Shadow': ('dps', 'priest'),
    'Feral': ('dps', 'druid'),
    'Bear': ('tank', 'druid')
}

raid_abbrev = {
    'Molten Core': 'mc',
    'Blackwing Lair': 'bwl',
    "Zul'Gurub": 'zg'
}


def read_raids():
    raids = []
    for filename in os.listdir(raid_dir):
        with open(os.path.join(raid_dir, filename), encoding='utf-8') as signups_file:
            signups_raw = signups_file.read()
            for (name, date, signees) in parse_raids(signups_raw):
                if not any((o_name, o_date, _) for (o_name, o_date, _) in raids if
                           name == o_name and date == o_date):  # O(n^2), I don't even care.
                    raids.append((name, date, signees))
    return raids


def read_raid(filename):
    with open(filename, encoding='utf-8') as signups_file:
        signups_raw = signups_file.readlines()
        return parse_raid(signups_raw)


def parse_raids(blob):
    raids = []
    is_raid_line = False
    raid_lines = []
    for line in blob.splitlines():
        if is_raid_line:
            if line == '-- end --':
                is_raid_line = False
            else:
                raid_lines[-1].append(line)
        else:
            if line == '-- start --':
                raid_lines.append([])
                is_raid_line = True

    for raid_line in raid_lines:
        raids.append(parse_raid(raid_line))

    return raids


def get_kruisvaarders():
    with open(kruisvaarders_filename, encoding='utf-8') as kruisvaarders_file:
        return [x.strip() for x in kruisvaarders_file.readlines()]


def parse_raid(blob):
    signups = []
    raid_name, raid_date = tuple(blob[1].split(',')[:2])
    raid_name = raid_abbrev[raid_name]
    dd, mm, yyyy = tuple(map(int, raid_date.split('-')))
    raid_date = datetime(yyyy, mm, dd).date()
    kruisvaarders = get_kruisvaarders()
    for line in blob[2:-4]:
        for charcol in line.strip().split(',')[1:]:
            if charcol:
                charname, roleclass = tuple(charcol.split('--')[2:])
                role, clazz = parse_mapping.get(roleclass, ('dps', roleclass.lower()))
                charname = _get_charname(charname.strip('*'))
                signups.append({'name': charname, 'class': clazz, 'role': role, 'signup_status': 'Accepted',
                                'is_kruisvaarder': charname in kruisvaarders})
    for line in blob[-4:]:
        parts = line.split(',')
        signup_status = parts[0]
        for part in parts[1:]:
            if part:
                charname = _get_charname(part.split('--')[-2].strip('*'))
                signups.append(
                    {'name': charname, 'signup_status': signup_status, 'is_kruisvaarder': charname in kruisvaarders})

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
