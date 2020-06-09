from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time"
        subname = 'remove'
        description = 'Verwijder een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname=subname, description=description, argformat=argformat)

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, **kwargs):
        self.respond(await self.events_resource.remove_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime))
