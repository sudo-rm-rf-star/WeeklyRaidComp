from src.logic.enums.Role import Role
from src.logic.enums.Class import Class
from src.logic.enums.SignupStatus import SignupStatus

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
    Role.TANK: 'Tank',
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
        Class.PALADIN: 'Retri',
        Class.DRUID: 'Feral'
    },
    Role.TANK: {
        Class.WARRIOR: 'ProtWarrior',
        Class.PALADIN: 'ProtPaladin',
        Class.DRUID: 'Bear'
    },
    Role.HEALER: {
        Class.PRIEST: 'Priest',
        Class.PALADIN: 'HolyPaladin',
        Class.DRUID: 'RestoDruid'
    }
}

SIGNUP_STATUS_EMOJI = {
    SignupStatus.ACCEPT: 'Accept',
    SignupStatus.DECLINE: 'Decline',
    SignupStatus.BENCH: 'Bench',
    SignupStatus.LATE: 'Late',
    SignupStatus.TENTATIVE: 'Tentative',
    SignupStatus.UNDECIDED: 'Unknown',
}

EMOJI_SIGNUP_STATUS = {v: k for k, v in SIGNUP_STATUS_EMOJI.items()}
