from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime
from exceptions.InvalidArgumentException import InvalidArgumentException


class CreateRaidCommand(RaidCommand):
    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time"

    async def execute(self, raid_name, raid_datetime, is_open, **kwargs):
        if raid_datetime < DateOptionalTime.now():
            raise InvalidArgumentException('Raid event must be in future')
        await self.create_raid(raid_name, raid_datetime, is_open)
