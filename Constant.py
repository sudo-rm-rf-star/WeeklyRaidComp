# If you feel crazy and don't want to go as 39 you can change me...
expected_raid_size = 40
out_filename = "roster.xlsx"

role_weight = 0.6
class_role_weight = 0.2
guild_role_weight = 0.2

guild_role_priority = {
    'Hertog': 1,
    'Kruisvaarder': 1,
    'Ridder': 1
}

pref_per_role = {
    'tank': 4,
    'healer': 9,
    'dps': 27
}

min_per_class_role = {
    'dps': {
        'druid': 0,
        'paladin': 0,
        'rogue': 3,
        'warrior': 3,
        'hunter': 4,
        'warlock': 4,
        'mage': 4,
        'priest': 0,
    },
    'healer': {
        'priest': 3,
        'druid': 1,
        'paladin': 1,
    },
    'tank': {
        'warrior': 2,
        'druid': 0,
        'paladin': 0,
    }
}

max_per_class_role = {
    'dps': {
        'druid': 1,
        'paladin': 1,
        'rogue': 6,
        'warrior': 6,
        'hunter': 6,
        'warlock': 6,
        'mage': 8,
        'priest': 0,
    },
    'healer': {
        'priest': 7,
        'druid': 2,
        'paladin': 2,
    },
    'tank': {
        'warrior': 4,
        'druid': 1,
        'paladin': 1,
    }
}

color_per_class = {
    'mage': '#69CCF0',
    'rogue': '#FFF569',
    'warrior': '#C79C6E',
    'paladin': '#F58CBA',
    #'priest': '#FFFFFF',
    'priest': '#D3D3D3',
    'druid': '#FF7D0A',
    'warlock': '#9482C9',
    'hunter': '#ABD473'
}
