from enum import Enum, auto


class RaidTeamControlAction(Enum):
    AddRaid = "Create a new raid event."

    @staticmethod
    def names():
        return list(map(lambda c: c.name, RaidTeamControlAction))
