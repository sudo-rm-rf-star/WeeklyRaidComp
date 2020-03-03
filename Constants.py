# If you feel crazy and don't want to go as 39 you can change me...
expected_raid_size = 40
out_filename = "roster.xlsx"

min_per_role = {
    'tank': 3,
    'healer': 8,
    'dps': 26
}

max_per_role = {
    'tank': 5,
    'healer': 10,
    'dps': 30
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
        'mage': 9,
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
