from src.commands.roster.UpdateRosterCommand import UpdateRosterCommand
from src.logic.RaidEvent import RaidEvent
from src.logic.enums.RosterStatus import RosterStatus
from typing import Optional


class BenchPlayerCommand(UpdateRosterCommand):
    def __init__(self):
        subname = 'bench'
        description = 'Plaats een speler op standby'
        super(BenchPlayerCommand, self).__init__(subname, description)

    def update_command(self, raid_event: RaidEvent, player_name: str, team_index: Optional[int]) -> None:
        raid_event.add_player_to_roster(player_name, RosterStatus.EXTRA)
