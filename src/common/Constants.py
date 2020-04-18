import os
from src.raids import MCConstants
from src.raids import BWLConstants
from src.raids import ZGConstants

BOT_NAME = 'DokBot'
MAINTAINER = 'Dok'
RAID_STORAGE = os.path.join('data', 'raids')
ROSTER_STORAGE = os.path.join('data', 'rosters')
RAID_INFO_EMBEDS = os.path.join('data', 'embeds', 'raid-info.json')
EVENTS_CHANNEL = 'raid-events'
RAID_HELPER_BOT = 'Raid-Helper'
GUILD = 'De Rode Ridders'
DATE_FORMAT = '%d-%m-%Y'
USE_SIGNUP_HISTORY = False
VERBOSE = False
OFFICER_RANK = 'Hertog'
SUPPORTED_RAIDS = ['mc', 'bwl', 'zg']

role_to_emoji_name = {
    'tank': 'Tanks',
    'healer': 'Healer',
    'ranged': 'Ranged',
    'melee': 'Melee'
}

CALENDAR_EMOJI = 'CMcalendar'
CLOCK_EMOJI = 'CMclock'
SIGNUPS_EMOJI = 'signups'
TEAM_EMOJI = 'group'
BENCH_EMOJI = "Bench"
MISSING_EMOJI = "Missing"

WEEKDAYS = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']

pref_per_role = {
    'mc': MCConstants.pref_per_role,
    'bwl': BWLConstants.pref_per_role,
    'zg': ZGConstants.pref_per_role
}

min_per_class_role = {
    'mc': MCConstants.min_per_class_role,
    'bwl': BWLConstants.min_per_class_role,
    'zg': ZGConstants.min_per_class_role
}

max_per_class_role = {
    'mc': MCConstants.max_per_class_role,
    'bwl': BWLConstants.max_per_class_role,
    'zg': ZGConstants.max_per_class_role
}

color_per_class = {
    'mage': '#69CCF0',
    'rogue': '#FFF569',
    'warrior': '#C79C6E',
    'paladin': '#F58CBA',
    # 'priest': '#FFFFFF',
    'priest': '#D3D3D3',
    'druid': '#FF7D0A',
    'warlock': '#9482C9',
    'hunter': '#ABD473',
}

DEFAULT_COLOR = '#FFFFFF'

signup_status_to_role_class = {
    'Tank': ('tank', 'warrior'),
    'Warrior': ('melee', 'warrior'),

    'HolyPaladin': ('healer', 'paladin'),
    'ProtPaladin': ('tank', 'paladin'),
    'Retri': ('melee', 'paladin'),

    'RestoDruid': ('healer', 'druid'),
    'Feral': ('melee', 'druid'),
    'Bear': ('tank', 'druid'),
    'Balance': ('ranged', 'druid'),

    'Priest': ('healer', 'priest'),
    'Shadow': ('ranged', 'priest'),

    'Hunter': ('ranged', 'hunter'),
    'Mage': ('ranged', 'mage'),
    'Warlock': ('ranged', 'warlock'),
    'Rogue': ('melee', 'rogue')
}

raid_abbrev_long = {
    'Molten Core': 'mc',
    'Blackwing Lair': 'bwl',
    "Zul'Gurub": 'zg'
}

raid_abbrev_short = {
    'moltencore': 'mc',
    'blackwinglair': 'bwl',
    "zulgurub": 'zg'
}

abbrev_to_full = {v: k for k, v in raid_abbrev_long.items()}
