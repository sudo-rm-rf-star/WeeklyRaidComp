from src.commands.UpdateRosterCommand import UpdateRosterCommand


class BenchPlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'bench'
        description = 'Plaats een speler op standby'
        super(BenchPlayerCommand, self).__init__(subname, description)

    def update_command(self, roster, player):
        return roster.bench_player(player)
