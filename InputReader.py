import re
from pandas import DataFrame, read_csv, merge
import os
from collections import defaultdict

signups_filename = 'data/signups-test.txt'
guild_members_filename = 'data/guild-members.csv'
statuses = ['Accepted', 'Declined', 'Tentative']


def get_signees():
    guild_members = read_csv(guild_members_filename)
    signup_statuses = read_signups()
    assert_guild_members_completeness(guild_members, signup_statuses)
    signees = merge(signup_statuses, guild_members, on=['name'], how='left')
    return signees


def assert_guild_members_completeness(guild_members, signup_statuses):
    guild_members = set(guild_members['name'])
    signees = set(signup_statuses['name'])
    non_existent_guild_members = signees.difference(guild_members)
    if len(non_existent_guild_members) > 0:
        print(f"Please add {', '.join(non_existent_guild_members)} to {guild_members_filename} before proceeding.")
        exit(1)


def read_signups():
    cur_status = None
    signups = []
    standby_counts = read_standby_count()
    for row in open(signups_filename, 'r', encoding='utf-8').readlines():
        row = row.strip()
        status = _read_status(row)
        if status:
            cur_status = status
        else:
            charname = _read_signup(row)
            if cur_status in ['Accepted', 'Tentative']:
                signups.append({'name': charname, 'signup_state': cur_status, 'standby_count': standby_counts[charname]})
    return DataFrame(signups)


def read_standby_count():
    dirname = 'history'
    standby_count = defaultdict(int)
    for filename in os.listdir(dirname):
        if filename.endswith('.csv'):
            for name in [row.strip().split(',')[-1] for row in open(os.path.join(dirname, filename)).readlines()][1:]:
                if name:
                    standby_count[name] += 1
    return standby_count


def _read_status(row):
    for status in statuses:
        if status in row:
            return status
    return None


def _read_signup(row):
    regex = r"[\wóòé']+"
    matches = re.findall(regex, row)
    if not (len(matches)):
        print(f"Failed to process {row}. Please contact Groovypanda")
        exit(1)

    charname = re.findall(regex, row)[0]
    return charname.capitalize()
