from enum import Enum


class SignupStatus(Enum):
    """ The number represents the priority a person gets in the raid depending on his signup state.
    A lower number equals a higher priority."""
    ACCEPT = 1
    UNDECIDED = 2
    LATE = 3
    BENCH = 4
    TENTATIVE = 5
    DECLINE = 6
    SWITCH_CHAR = 100  # A signup option for players to switch characters
    #  HELP = 100  # A signup option to show a help page

    def __lt__(self, other):
        return self.value < other.value
