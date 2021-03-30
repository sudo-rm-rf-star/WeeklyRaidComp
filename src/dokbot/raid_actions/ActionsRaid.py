from enum import Enum


class ActionsRaid(Enum):
    AddRaider = "Invite a new player to the raid."
    Accept = "Accept a player to the raid."
    Bench = "Bench a player for the raid."
    Decline = "Decline a player for the raid."
    OpenRaid = "Open this raid so that anyone can sign without invitation."
    SendReminder = "Send a reminder for invited players to signup."
    CreateRosterAutomatic = "Create a roster for this raid."
    CreateRosterManual = "Create a roster for this raid manually."
    RemoveRaid = "Remove this raid."

    @staticmethod
    def names():
        return list(map(lambda c: c.name, ActionsRaid))
