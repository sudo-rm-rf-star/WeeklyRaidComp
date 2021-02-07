from dokbot.commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class BenchPlayerCommand(UpdateRosterCommand):
    @classmethod
    def sub_name(cls) -> str: return "bench"

    @classmethod
    def description(cls) -> str: return "Bench a player for the raid"

    @classmethod
    def roster_choice(cls) -> RosterStatus: return RosterStatus.EXTRA
