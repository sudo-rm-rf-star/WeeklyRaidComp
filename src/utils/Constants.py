import os
BOT_NAME = 'DokBot'
BASE_GUILD_ID = 427579030322282509
MAINTAINER_ID = 229262793331703810
TESTER_ID = 582301840260071465
RAID_INFO_EMBEDS = os.path.join('css', 'embeds', 'raid-info.json')
RAID_HELPER_BOT = 'Raid-Helper'
DATE_FORMAT = '%d-%m-%Y'
INFO_CHANNEL = 'raid-info'  # TODO: This does not belong here...
TIME_FORMAT = '%H:%M'
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT
DATETIMESEC_FORMAT = '%d-%m-%Y %H:%M:%S'
FILE_DATETIME_FORMAT = DATETIME_FORMAT.replace(' ', '_').replace(':', '')
USE_SIGNUP_HISTORY = False
VERBOSE = False

raid_names = {
    'Molten Core': 'mc',
    'Blackwing Lair': 'bwl',
    "Zul'Gurub": 'zg',
    'Onyxia': 'ony',
    "Temple of Ahn'Qiraj": 'aq',
    "Ruins of Ahn'Qiraj": 'aq20',
    'Naxxramas': 'naxx'
}

full_raid_name = {v: k for k, v in raid_names.items()}
