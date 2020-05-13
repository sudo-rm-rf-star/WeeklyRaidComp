from commands.raid.RaidCommand import RaidCommand
from utils.Constants import OFFICER_RANK


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time [channel_name]"
        subname = 'create'
        description = 'Maak een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname, description, argformat, OFFICER_RANK)

    async def execute(self, raid_name, raid_datetime, **kwargs):
        self.respond(await self.events_resource.create_raid(raid_name, raid_datetime))
