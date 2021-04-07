from enum import Enum


class SignupStatus(Enum):
    Accept = 'Accept the raid invitation. You can attend the raid.'
    Bench = "Accept the raid invitation. By choosing this you indicate to the raid leader that you don't mind sitting on the bench if there are to few spots"
    Decline = 'Decline the raid invitation. You cannot attend.'
    Late = 'Accept the raid invitation, but you will be late.'
    Tentative = 'Accept the raid invitation, but you are not sure yet if you can attend.'
    SwitchSpec = 'Change your specialization'
    SwitchChar = 'Switch to a new character'
    AddChar = 'Add a character'
    RemoveChar = 'Remove a character'
    Unknown = f'Shows this help page. More questions? Contact an officer of your guild.'

    @staticmethod
    def names():
        return list(map(lambda c: c.name, SignupStatus))
