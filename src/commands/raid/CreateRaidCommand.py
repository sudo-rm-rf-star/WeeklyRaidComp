from commands.raid.RaidCommand import RaidCommand
from utils.Constants import MAINTAINER_ID, TESTER_ID
from utils.DiscordUtils import get_member_by_id


class CreateRaidCommand(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "create"

    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time"

    @classmethod
    def description(cls) -> str: return "Create a new event for a raid"

    async def execute(self, raid_name, raid_datetime, **kwargs):
        # raiders = self.get_raiders()
        raiders = [await get_member_by_id(self.discord_guild, MAINTAINER_ID), await get_member_by_id(self.discord_guild, TESTER_ID)]
        events_channel = await self.get_events_channel()
        response = await self.events_resource.create_raid(discord_guild=self.discord_guild, group_id=self._raidgroup.group_id, raid_name=raid_name,
                                                          raid_datetime=raid_datetime, raiders=raiders, events_channel=events_channel)
        self.respond(response)
