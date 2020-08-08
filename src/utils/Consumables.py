from logic.enums.Class import Class
from logic.enums.Role import Role

EXPECTED_CONSUMABLES = {
    'aq': [
        ([Role.MELEE, Role.TANK, Class.HUNTER], ["Nature Protection"]),
        ([Role.MELEE, Class.HUNTER], ["Elixir of the Mongoose", "Greater Agility"]),
        ([Role.MELEE], ["Elixir of the Giants"])
    ]
}

