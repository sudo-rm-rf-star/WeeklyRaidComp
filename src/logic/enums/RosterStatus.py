from enum import Enum


class RosterStatus(Enum):
    """ The number represents the priority a person gets in the raid depending on his roster state.
    A lower number equals a higher priority. This is only used when updating the roster which already has decided players.
    Players initially accepted get a higher priority"""
    ACCEPT = 1,
    EXTRA = 3,
    UNDECIDED = 2,
    DECLINE = 4

    def __new__(cls, *args, **kwargs):
        if isinstance(args, tuple):
            value = args[0]
        else:
            value = args

        super(RosterStatus, cls).__new__(value, **kwargs)
