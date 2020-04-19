from src.commands.UpdateRosterCommand import UpdateRosterCommand


class RemovePlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'remove'
        description = 'Haalt een speler uit de raid compositie'
        super(RemovePlayerCommand, self).__init__(subname, description)

    def update_command(self, roster, player):
        return roster.remove_player(player)
