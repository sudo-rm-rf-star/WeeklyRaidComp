from enum import Enum


class SignupStatus(Enum):
    """ The number represents the priority a person gets in the raid depending on his signup state.
    A lower number equals a higher priority."""
    ACCEPT = 1,
    UNDECIDED = 2,
    LATE = 3,
    BENCH = 4,
    TENTATIVE = 5,
    DECLINE = 6,

    def __lt__(self, other):
        return self.value < other.value
