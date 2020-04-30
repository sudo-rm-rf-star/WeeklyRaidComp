import os
from src.raids import MCConstants
from src.raids import BWLConstants
from src.raids import ZGConstants

BOT_NAME = 'DokBot'
MAINTAINER = 'Dok'
RAID_STORAGE = os.path.join('data', 'raids')
PLAYER_STORAGE = os.path.join('data', 'players')
RAID_INFO_EMBEDS = os.path.join('data', 'embeds', 'raid-info.json')
STORAGE_SUFFIX = '.csv'
EVENTS_CHANNEL = 'raid-signups'
INFO_CHANNEL = 'raid-info'
COMPS_CHANNEL = 'raid-comps'
# COMPS_CHANNEL = 'test'
LOGS_CHANNEL = 'bot-logs'
RAID_HELPER_BOT = 'Raid-Helper'
GUILD = 'De Rode Ridders'
DATE_FORMAT = '%d-%m-%Y'
TIME_FORMAT = '%H:%M'
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT
DATETIMESEC_FORMAT = '%d-%m-%Y %H:%M:%S'
FILE_DATETIME_FORMAT = DATETIME_FORMAT.replace(' ', '_').replace(':', '')
USE_SIGNUP_HISTORY = False
VERBOSE = False
OFFICER_RANK = 'Hertog'
SUPPORTED_RAIDS = ['mc', 'bwl', 'zg']
RAIDER_RANK = 'Kruisvaarder'
ZONE_ID = {
    'zg': 1003,
    'bwl': 1002,
    'mc': 1000
}

WARCRAFT_LOGS_GUILD_ID = 510080
WARCRAFT_LOGS_TEAM_ID = 29777


WEEKDAYS = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']

pref_per_role = {
    'mc': MCConstants.pref_per_role,
    'bwl': BWLConstants.pref_per_role,
    'zg': ZGConstants.pref_per_role
}

player_count = {
    raid: sum(key_counts.values()) for raid, key_counts in pref_per_role.items()
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

signup_choice_to_role_class = {
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
