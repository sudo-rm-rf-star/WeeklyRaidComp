from src.commands.roster.UpdateRosterCommand import UpdateRosterCommand
from src.logic.RaidEvent import RaidEvent
from src.logic.enums.RosterStatus import RosterStatus
from typing import Optional


class AcceptPlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'accept'
        description = 'Voeg een speler toe aan de raid compositie'
        super(AcceptPlayerCommand, self).__init__(subname, description)

    def update_command(self, raid_event: RaidEvent, player_name: str, team_index: Optional[int]) -> str:
        raid_event.add_player_to_roster(player_name, RosterStatus.ACCEPT)
        return f'Raid event for {raid_event.get_name()} on {raid_event.get_date()} has been successfully updated.'
