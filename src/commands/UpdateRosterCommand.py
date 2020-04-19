from src.commands.RosterCommand import RosterCommand
from src.exceptions.InternalBotException import InternalBotException
from src.common.Constants import OFFICER_RANK


class UpdateRosterCommand(RosterCommand):
    def __init__(self, subname, description):
        argformat = "raid_name player [raid_datetime][team_index]"
        required_rank = OFFICER_RANK
        allow_trough_approval = True
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank,
                                            allow_trough_approval)

    def update_command(self, roster, player):
        raise InternalBotException("Please specify logic for this command.")

    async def run(self, client, message, **kwargs):
        return self._run(client, **kwargs)

    async def _run(self, client, raid_name, raid_datetime, player, team_index):
        await self.update_datastores(client)
        rosters = self.load_rosters(raid_name, raid_datetime)
        roster = rosters.get(team_index)
        success, response = self.update_command(roster, player)
        if success:
            self.post_roster(client, rosters)
        return response
