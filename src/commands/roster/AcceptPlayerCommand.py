from commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class AcceptPlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'accept'
        description = 'Voeg een speler toe aan de raid compositie'
        super(AcceptPlayerCommand, self).__init__(subname=subname, description=description, roster_choice=RosterStatus.ACCEPT)
