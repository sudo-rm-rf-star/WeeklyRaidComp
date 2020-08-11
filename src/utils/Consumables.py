from logic.enums.Class import Class
from logic.enums.Role import Role

#  https://docs.google.com/spreadsheets/d/1JiwdusZfL_37YFjgHB3wPr0pdDgySBEyY6zRKoXEfgA/edit#gid=0
EXPECTED_CONSUMABLES = {
    'aq': [
        ([Role.MELEE, Role.TANK, Role.HEALER, Role.RANGED], ["Nature Protection"]),
        ([Role.MELEE, Class.HUNTER], ["Elixir of the Mongoose", "Greater Agility"]),
        ([Role.MELEE], ["Elixir of the Giants"]),
        ([Role.RANGED], ["Greater Arcane Elixir"]),
    ]
}

