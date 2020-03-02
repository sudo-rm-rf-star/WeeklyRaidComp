# coding=utf-8
import re
from collections import defaultdict
from Character import Character

characters_filename = 'data/char-class-role.csv'
signups_filename = 'data/signups.txt'
kruisvaarders_filename = 'data/kruisvaarders.txt'
statuses = ['Accepted', 'Declined', 'Tentative']


def read_signups():
    characters = read_characters()
    ksvaarders = read_kruisvaarders()
    return read_signups_helper(characters, ksvaarders)


def read_signups_helper(characters, kruisvaarders):
    cur_status = None
    signups = []
    for row in open(signups_filename, 'r').readlines():
        row = row.strip()
        status = _read_status(row)
        if status:
            cur_status = status
        else:
            charname = _read_signup(row)
            if not charname in characters:
                print(f"Please add {row} to the {characters_filename}.")
                exit(1)
            if not charname in kruisvaarders:
                print(f"Please add {row} to the {kruisvaarders_filename}.")
                is_kruisvaarder = False
            else:
                is_kruisvaarder = bool(kruisvaarders[charname])

            wowclass, wowrole = characters[charname]
            signup = Character(charname, wowclass, wowrole, is_kruisvaarder, cur_status)
            signups.append(signup)
    return signups


def read_characters():
    chars = defaultdict()
    for row in [row.split() for row in open(characters_filename, 'r').readlines()]:
        chars[row[0].lower()] = (row[1], row[2])
    return chars


def read_kruisvaarders():
    chars = defaultdict()
    for row in [row.split() for row in open(kruisvaarders_filename, 'r').readlines()]:
        chars[row[0].lower()] = row[1]
    return chars


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
    else:
        charname = re.findall(regex, row)[0]

    return charname.lower()
