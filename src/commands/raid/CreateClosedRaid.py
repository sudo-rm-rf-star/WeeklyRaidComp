from commands.raid.CreateRaidCommand import CreateRaidCommand


class CreateClosedRaid(CreateRaidCommand):
    @classmethod
    def subname(cls) -> str: return "create-closed"

    @classmethod
    def description(cls) -> str: return "Create a new event for a raid. This creates a closed event for which only people in the raidgroup can join."

    async def execute(self, raid_name, raid_datetime, **kwargs):
        await super(CreateClosedRaid, self).execute(raid_name=raid_name, raid_datetime=raid_datetime, is_open=False)
