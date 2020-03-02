#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import random
from collections import defaultdict
import Character
import InputReader


characters_filename = 'char-class-role.csv'
signups_filename = 'attendees.txt'
kruisvaarders_filename = 'kruisvaarders.txt'
statuses = ['Accepted', 'Declined', 'Tentative']

chars_per_role = {
        'tank': 4,
        'healer': 9,
        'dps': 27
}

pref_per_class_role = {
        ('druid', 'dps'): 1,
        ('rogue', 'dps'): 4,
        ('warrior', 'dps'): 4,
        ('paladin', 'dps'): 1,
        ('hunter', 'dps'): 4,

        ('mage', 'dps'): 7,
        ('priest', 'dps'): 1,
        ('warlock', 'dps'): 4,

        ('warrior', 'tank'): 2,
        ('druid', 'tank'): 1,
        ('paladin', 'tank'): 1,

        ('priest', 'healer'): 4,
        ('druid', 'healer'): 2,
        ('paladin', 'healer'): 2,
}

def read_status(row):
    for status in statuses:
        if status in row:
            return status
    return None

def read_signup(row):
    regex = r"[\wóòé']+"
    matches = re.findall(regex, row)
    if not(len(matches)):
        print(f"Failed to process {row}. Please contact Groovypanda")
        exit(1)
    else:
        charname = re.findall(regex, row)[0]

    return charname.lower()



def make_roster():
    characters = read_characters()
    kruisvaarders = read_kruisvaarders()
    signups = read_signups(characters, kruisvaarders)
    random.shuffle(signups) ## Introduce some randomness
    score_signups(signups)

    attendees = []
    bench = []

    while len(attendees) != 40:
        attendees

    print(signups)

def score_signups(signups):
    for signup in signups:
        signup.append(1 if signup[3] else 0.5)
    signups.sort(key=lambda x: x[-1])


if __name__ == '__main__':
    make_roster()




