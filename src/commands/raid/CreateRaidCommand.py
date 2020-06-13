from commands.raid.RaidCommand import RaidCommand


class CreateRaidCommand(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "create"

    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time"

    @classmethod
    def description(cls) -> str: return "Create a new event for a raid"

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raiders = self.get_raiders()
        self.respond(
            await self.events_resource.create_raid(self.discord_guild, self._raidgroup.group_id, raid_name, raid_datetime, raiders, self.get_events_channel()))
