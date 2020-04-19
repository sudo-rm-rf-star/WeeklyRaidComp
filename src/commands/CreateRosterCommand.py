from src.commands.RosterCommand import RosterCommand
from src.exceptions.EventDoesNotExistException import EventDoesNotExistException
from src.exceptions.EventAlreadyExistsException import EventAlreadyExistsException
from src.common.Constants import abbrev_to_full
from src.common.Utils import from_datetime
from src.logic.Rosters import Rosters
from src.logic.Raid import Raid


class CreateRosterCommand(RosterCommand):
    def __init__(self):
        argformat = "raid_name [raid_datetime]"
        subname = 'create'
        description = 'Maakt een raid compositie voor een event'
        super(RosterCommand, self).__init__('roster', subname, description, argformat)

    async def run(self, client, message, **kwargs):
        return await self._run(client, message, **kwargs)

    async def _run(self, client, message, raid_name, raid_datetime):
        await self.update_datastores(client)
        try:
            rosters = self.load_rosters(raid_name, raid_datetime)
            raise EventAlreadyExistsException(rosters.raid_name, rosters.raid_datetime)
        except EventDoesNotExistException:
            raid = Raid.load(raid_name, raid_datetime)
            rosters = Rosters.compose(raid)
            await self.post_roster(client, rosters)
            return f"Created a roster for {abbrev_to_full[rosters.raid_name]} on {from_datetime(rosters.raid_datetime)}"
