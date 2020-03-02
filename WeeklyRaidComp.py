#!/usr/bin/python
# coding=utf-8


import random
from InputReader import read_signups

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


def make_roster():
    signups = read_signups()
    random.shuffle(signups)  # Introduce some randomness
    signups.sort()
    print(signups)


if __name__ == '__main__':
    make_roster()
