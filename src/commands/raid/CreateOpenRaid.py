from commands.raid.CreateRaidCommand import CreateRaidCommand


class CreateOpenRaid(CreateRaidCommand):
    @classmethod
    def subname(cls) -> str: return "create-open"

    @classmethod
    def description(cls) -> str: return "Create a new event for a raid. This creates an open event for anyone can join."

    async def execute(self, raid_name, raid_datetime, **kwargs):
        await super(CreateOpenRaid, self).execute(raid_name=raid_name, raid_datetime=raid_datetime, is_open=True)
