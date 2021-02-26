from enum import Enum


class RaidControlAction(Enum):
    AddRaid = "Invite a player to the raid."

    @staticmethod
    def names():
        return list(map(lambda c: c.name, RaidTeamControlAction))
