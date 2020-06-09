from commands.raid.RaidCommand import RaidCommand


class CreateRaidCommand(RaidCommand):
    def __init__(self):
        argformat = "raid_name raid_date raid_time [channel_name]"
        subname = 'create'
        description = 'Maak een event voor een raid'
        super(CreateRaidCommand, self).__init__(subname=subname, description=description, argformat=argformat)

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raiders = self.get_raiders()
        self.respond(
            await self.events_resource.create_raid(self.discord_guild, self._raidgroup.group_id, raid_name, raid_datetime, raiders, self.get_events_channel()))
