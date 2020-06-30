from commands.raid.RaidCommand import RaidCommand


class CreateRaidCommand(RaidCommand):
    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time"

    @classmethod
    def description(cls) -> str: return "Create a new event for a raid. This creates an open event for anyone can join."

    async def execute(self, raid_name, raid_datetime, is_open, **kwargs):
        events_channel = await self.get_events_channel()
        raid_event, response = await self.events_resource.create_raid(discord_guild=self.discord_guild, group_id=self._raidgroup.group_id, raid_name=raid_name,
                                                                      raid_datetime=raid_datetime, events_channel=events_channel, is_open=is_open)
        if response:
            self.respond(response)
        if raid_event:
            raiders = await self.get_raiders()
            await self.send_raid_notification(raid_event=raid_event, raiders=raiders)
