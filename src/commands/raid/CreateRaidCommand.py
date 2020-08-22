from commands.raid.RaidCommand import RaidCommand


class CreateRaidCommand(RaidCommand):
    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time"

    async def execute(self, raid_name, raid_datetime, is_open, **kwargs):
        await self.create_raid(raid_name, raid_datetime, is_open)
