from enum import Enum


class SignupStatus(Enum):
    Accept = 'Accept the raid invitation. You can attend the raid.'
    Bench = 'Accept the raid invitation, but other players can have priority on your spot.'
    Decline = 'Decline the raid invitation. You cannot attend.'
    Late = 'Accept the raid invitation, but you will be late.'
    Tentative = 'Accept the raid invitation, but you are unsure if you can attend the raid. Once you are sure, you can choose a new status.'
    SwitchChar = 'Sign with another character. If you already signed with another character, you will keep the signup status.'
    Unknown = f'Shows this help page. More questions? Contact an officer of your guild.'

    @staticmethod
    def names():
        return list(map(lambda c: c.name, SignupStatus))
