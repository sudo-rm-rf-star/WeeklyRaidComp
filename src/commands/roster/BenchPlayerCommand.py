from commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class BenchPlayerCommand(UpdateRosterCommand):
    @classmethod
    def subname(cls) -> str: return "accept"

    @classmethod
    def description(cls) -> str: return "Bench a player for the raid"

    @classmethod
    def roster_choice(cls) -> RosterStatus: return RosterStatus.EXTRA
