from dokbot.commands.raid.RaidCog import RaidCog
from exceptions.InvalidInputException import InvalidInputException
from datetime import datetime


class CreateRaidCommand(RaidCog):
    @classmethod
    def argformat(cls) -> str: return "raid_name raid_datetime"

    async def execute(self, raid_name, raid_datetime, is_open, **kwargs):
        if raid_datetime < datetime.now():
            raise InvalidInputException('Raid event must be in future')
        await self.create_raid(raid_name, raid_datetime, is_open)
