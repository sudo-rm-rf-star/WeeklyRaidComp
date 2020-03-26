expected_raid_size = 40

raid = 'bwl'

out_filename = "roster.xlsx"

pref_per_role = {
    'bwl': {
        'tank': 4,
        'healer': 10,
        'dps': 26
    },
    'mc': {
        'tank': 4,
        'healer': 8,
        'dps': 28
    }
}

# notities mertin
# pref 2 pallys (don't care on role)
# pref feral druids
# pref boomkin
# pref 2 dwarf priest
# spreek met wisear
min_per_class_role = {
    'bwl': {
        'dps': {
            'druid': 1,
            'paladin': 0,
            'rogue': 2,
            'warrior': 2,
            'hunter': 4,
            'warlock': 2,
            'mage': 4,
            'priest': 1,
        },
        'healer': {
            'priest': 3,
            'druid': 3,
            'paladin': 3,
        },
        'tank': {
            'warrior': 1,
            'druid': 0,
            'paladin': 0,
        }
    },
    'mc': {
        'dps': {
            'druid': 1,
            'paladin': 0,
            'rogue': 4,
            'warrior': 4,
            'hunter': 4,
            'warlock': 2,
            'mage': 4,
            'priest': 1,
        },
        'healer': {
            'priest': 3,
            'druid': 3,
            'paladin': 3,
        },
        'tank': {
            'warrior': 1,
            'druid': 0,
            'paladin': 0,
        }
    }
}

max_per_class_role = {
    'bwl': {
        'dps': {
            'druid': 2,
            'paladin': 1,
            'rogue': 6,
            'warrior': 6,
            'hunter': 6,
            'warlock': 6,
            'mage': 7,
            'priest': 1,
        },
        'healer': {
            'priest': 6,
            'druid': 4,
            'paladin': 5,
        },
        'tank': {
            'warrior': 4,
            'druid': 3,
            'paladin': 1,
        }
    },
    'mc': {
        'dps': {
            'druid': 2,
            'paladin': 1,
            'rogue': 6,
            'warrior': 6,
            'hunter': 6,
            'warlock': 6,
            'mage': 8,
            'priest': 1,
        },
        'healer': {
            'priest': 6,
            'druid': 4,
            'paladin': 5,
        },
        'tank': {
            'warrior': 4,
            'druid': 3,
            'paladin': 1,
        }
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
    'hunter': '#ABD473',
    'unknown': '#FFFFFF'
}
