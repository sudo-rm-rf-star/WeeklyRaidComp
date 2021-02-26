from dokbot.commands.raidteam.RaidTeamCog import RaidTeamCog
from datetime import datetime


class RemoveRaidCommand(RaidTeamCog):
    @classmethod
    def sub_name(cls) -> str:
        return "remove"

    @classmethod
    def argformat(cls) -> str:
        return "raid_name [raid_datetime]"

    @classmethod
    def description(cls) -> str:
        return "Remove the event for a raid"

    async def execute(self, raid_name: str, raid_datetime: datetime, **kwargs):
        raid_event = await self.get_raid_event(raid_name, raid_datetime)
        self.raids_resource.remove_raid(raid_event)
