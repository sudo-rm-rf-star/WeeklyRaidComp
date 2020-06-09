from commands.roster.UpdateRosterCommand import UpdateRosterCommand
from logic.enums.RosterStatus import RosterStatus


class DeclinePlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'decline'
        description = 'Haal een speler uit de raid compositie'
        super(DeclinePlayerCommand, self).__init__(subname=subname, description=description, roster_choice=RosterStatus.DECLINE)
