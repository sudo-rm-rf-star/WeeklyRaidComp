from commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class BenchPlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'bench'
        description = 'Plaats een speler op standby'
        super(BenchPlayerCommand, self).__init__(subname, description, RosterStatus.EXTRA)
