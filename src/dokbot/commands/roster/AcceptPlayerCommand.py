from dokbot.commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class AcceptPlayerCommand(UpdateRosterCommand):
    @classmethod
    def sub_name(cls) -> str: return "accept"

    @classmethod
    def description(cls) -> str: return "Accept a player to the raid"

    @classmethod
    def roster_choice(cls) -> RosterStatus: return RosterStatus.ACCEPT

