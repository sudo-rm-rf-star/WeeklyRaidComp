from enum import Enum


class ActionsRaidTeam(Enum):
    AddRaid = "Create a new raid event."
    ManageRaid = "Manage a future raid event."
    AddRaider = "Add a raider who gets invited to every new raid."
    AddRaiders = "Add a group of raiders who get invited to every new raid."
    RemoveRaider = "Remove a raider who gets invited to every new raid."
    AddRaidLeader = "Add a raidleader who can manage this raidteam."
    ShowRaidTeam = "Show the players in this raidteam."
    SwitchRaidTeam = "Manage another raidteam."
    HelpRaidTeam = "Shows this message"

    @staticmethod
    def names():
        return list(map(lambda c: c.name, ActionsRaidTeam))
