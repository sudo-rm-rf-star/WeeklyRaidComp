from commands.raid.RaidCommand import RaidCommand


class ShowRaidEvent(RaidCommand):
    @classmethod
    def argformat(cls) -> str:
        return "raid_name [raid_date][raid_time]"

    @classmethod
    def description(cls) -> str:
        return "Posts another message for the given event"

    @classmethod
    def subname(cls) -> str:
        return "show"

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        await self.send_raid_message(self.channel, raid_event)
        self.events_resource.update_raid(self.discord_guild, raid_event)
