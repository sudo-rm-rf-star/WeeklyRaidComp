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

# These can be removed...
SIGNUP_STATUS_EMOJI = {
    SignupStatus.ACCEPT: 'Accept',
    SignupStatus.BENCH: 'Bench',
    SignupStatus.DECLINE: 'Decline',
    SignupStatus.LATE: 'Late',
    SignupStatus.TENTATIVE: 'Tentative',
    SignupStatus.SWITCH_CHAR: 'SwitchChar',
    SignupStatus.UNDECIDED: 'Unknown',
}

SIGNUP_STATUS_HELP = {
    SignupStatus.ACCEPT: 'Accept the raid invitation. You can attend the raid.',
    SignupStatus.BENCH: 'Accept the raid invitation, but other players can have priority on your spot.',
    SignupStatus.DECLINE: 'Decline the raid invitation. You cannot attend.',
    SignupStatus.LATE: 'Accept the raid invitation, but you will be late.',
    SignupStatus.TENTATIVE: 'Accept the raid invitation, but you are unsure if you can attend the raid. '
                            'Once you are sure, you can choose a new status.',
    SignupStatus.SWITCH_CHAR: 'Sign with another character. '
                              'If you already signed with another character, you will keep the signup status.',
    SignupStatus.UNDECIDED: f'Shows this help page. More questions? Contact an officer of your guild.',
}

EMOJI_SIGNUP_STATUS = {v: k for k, v in SIGNUP_STATUS_EMOJI.items()}
