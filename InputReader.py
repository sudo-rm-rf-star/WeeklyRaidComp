import re
from pandas import DataFrame
import os
from collections import defaultdict
from Constant import raid

signups_filename = f"data/signups.csv"
standby_history = f"history/standby/{raid}"
kruisvaarders_filename = 'data/kruisvaarders.txt'
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


def assert_guild_members_completeness(guild_members, signup_statuses):
    guild_members = set(guild_members['name'])
    signees = set(signup_statuses['name'])
    non_existent_guild_members = signees.difference(guild_members)
    if len(non_existent_guild_members) > 0:
        print(f"Please add {', '.join(non_existent_guild_members)} to {kruisvaarders_filename} before proceeding.")
        exit(1)


def get_signees():
    standby_counts = read_standby_count()
    print(standby_counts)
    signups = []
    with open(signups_filename, encoding='utf-8') as signups_file:
        kruisvaarders = [line.strip() for line in open(kruisvaarders_filename, encoding='utf-8').readlines()]
        signups_raw = signups_file.readlines()
        for benched in signups_raw[-3].strip().split(',')[1:]:
            if benched:
                charname = _get_charname(benched.split('--')[2])
                signups.append({'name': charname, 'kruisvaarder': False, 'class': 'unknown'})
        for line in signups_raw[2:-4]:
            for charcol in line.strip().split(',')[1:]:
                if charcol:
                    charname, roleclass = tuple(charcol.split('--')[2:])
                    role, clazz = parse_mapping.get(roleclass, ('dps', roleclass.lower()))
                    charname = _get_charname(charname)
                    signups.append({'name': charname, 'standby_count': standby_counts[charname], 'class': clazz, 'role': role, 'kruisvaarder': charname in kruisvaarders})
    return DataFrame(signups)


def read_standby_count():
    standby_count = defaultdict(int)
    for filename in os.listdir(standby_history):
        for name in [row.strip().split(',')[-1] for row in
                     open(os.path.join(standby_history, filename)).readlines()][1:]:
            if name:
                standby_count[name] += 1
    return standby_count


def _read_status(row):
    for status in statuses:
        if status in row:
            return status
    return None


def _get_charname(row):
    regex = r"[\wóòé']+"
    matches = re.findall(regex, row)
    if not (len(matches)):
        print(f"Failed to process {row}. Please contact Groovypanda")
        exit(1)

    charname = re.findall(regex, row)[0]
    return charname.capitalize()
