from logic.enums.Role import Role
from logic.enums.Class import Class
from logic.enums.SignupStatus import SignupStatus

CALENDAR_EMOJI = 'CMcalendar'
CLOCK_EMOJI = 'CMclock'
SIGNUPS_EMOJI = 'signups'
TEAM_EMOJI = 'group'
BENCH_EMOJI = "Bench"
LATE_EMOJI = 'Late'
TENTATIVE_EMOJI = 'Tentative'
MISSING_EMOJI = 'Missing'

ROLE_EMOJI = {
    Role.RANGED: 'Ranged',
    Role.MELEE: 'Melee',
    Role.TANK: 'ProtWarrior',
    Role.HEALER: 'Healer'
}

ROLE_CLASS_EMOJI = {
    Role.RANGED: {
        Class.MAGE: 'Mage',
        Class.WARLOCK: 'Warlock',
        Class.HUNTER: 'Hunter',
        Class.PRIEST: 'Shadow',
        Class.DRUID: 'Balance'
    },
    Role.MELEE: {
        Class.WARRIOR: 'Warrior',
        Class.ROGUE: 'Rogue',
        Class.PALADIN: 'Retribution_Paladin',
        Class.DRUID: 'Feral_Druid'
    },
    Role.TANK: {
        Class.WARRIOR: 'ProtWarrior',
        Class.PALADIN: 'ProtPaladin',
        Class.DRUID: 'Bear_Druid'
    },
    Role.HEALER: {
        Class.PRIEST: 'Priest',
        Class.PALADIN: 'Holy_Paladin',
        Class.DRUID: 'RestoDruid'
    }
}
