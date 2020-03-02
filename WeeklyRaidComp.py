#!/usr/bin/python
# coding=utf-8


import random
from InputReader import read_signups

expected_raid_size = 40

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


def evaluate(signup, desperate_roles=None):
    desperate_roles = [] if not desperate_roles else desperate_roles
    if signup.event_status != 'Accepted':
        return False
    if chars_per_role[signup.role] == 0:
        return False
    if (pref_per_class_role[(signup.clss, signup.role)] == 0 or not signup.is_kruisvaarder) and not signup.role not in desperate_roles:
        return False
    return True


def pick(signup):
    chars_per_role[signup.role] -= 1
    pref_per_class_role[(signup.clss, signup.role)] -= 1


def make_roster():
    signups = read_signups()
    print(f"{len(signups)} geinterreseerden")
    random.shuffle(signups)  # Introduce some randomness
    attendees = []
    benched = []

    while len(signups) > 0:
        signup = signups.pop()
        should_pick = evaluate(signup)
        if should_pick and len(attendees) < expected_raid_size:
            attendees.append(signup)
            pick(signup)
        else:
            benched.append(signup)

    desperate_roles = [role for (role, num_unfilled) in chars_per_role.items() if num_unfilled > 0]
    while expected_raid_size != len(attendees):
        signup = benched.pop()
        should_pick = evaluate(signup, desperate_roles=desperate_roles)
        if should_pick:
            attendees.append(signup)
            pick(signup)
        else:
            benched.append(signup)

    return attendees, benched

def print_roster(attendees, benched):
    attendees.sort(key=lambda char: (char.role, char.clss))
    benched.sort(key=lambda char: (char.role, char.clss))
    print(f"==== Raid Team - {len(attendees)} spelers ====")
    print("\n".join(map(str, attendees)))
    print(f"==== Bank - {len(benched)} spelers ====")
    print("\n".join(map(str, benched)))

if __name__ == '__main__':
    attendees, benched = make_roster()
    print_roster(attendees, benched)
