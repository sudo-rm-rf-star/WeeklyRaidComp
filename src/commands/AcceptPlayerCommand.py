from src.commands.UpdateRosterCommand import UpdateRosterCommand


class AcceptPlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'accept'
        description = 'Voegt een speler toe aan de raid compositie'
        super(AcceptPlayerCommand, self).__init__(subname, description)

    def update_command(self, roster, player):
        return roster.accept_player(player)
