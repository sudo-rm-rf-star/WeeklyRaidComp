from dokbot.commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class DeclinePlayerCommand(UpdateRosterCommand):
    @classmethod
    def sub_name(cls) -> str: return "decline"

    @classmethod
    def description(cls) -> str: return "Decline a player for the raid"

    @classmethod
    def roster_choice(cls) -> RosterStatus: return RosterStatus.DECLINE
