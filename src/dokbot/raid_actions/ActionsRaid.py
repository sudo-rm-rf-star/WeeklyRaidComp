from enum import Enum


class ActionsRaid(Enum):
    InviteRaider = "Invite a new player to the raid."
    RosterAccept = "Accept a player to the raid."
    RosterBench = "Bench a player for the raid."
    RosterDecline = "Decline a player for the raid."
    OpenRaid = "Open this raid so that anyone can sign without invitation."
    SendReminder = "Send a reminder for invited players to signup."
    CreateRoster = "Create a roster for this raid."
    RemoveRaid = "Remove this raid."
    HelpRaid = "Shows this message"

    @staticmethod
    def names():
        return list(map(lambda c: c.name, ActionsRaid))
