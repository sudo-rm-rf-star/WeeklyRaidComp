from src.raids import MCConstants
from src.raids import BWLConstants
from src.raids import ZGConstants

USE_SIGNUP_HISTORY = False
VERBOSE = False

supported_raids = ['mc', 'bwl', 'zg']

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
