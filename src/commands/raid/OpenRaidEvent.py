from commands.raid.RaidCommand import RaidCommand


class OpenRaidEvent(RaidCommand):
    @classmethod
    def subname(cls) -> str: return "open"

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_date][raid_time]"

    @classmethod
    def description(cls) -> str: return "Opens an event so that anyone can join. This will add signup buttons to the event message."

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        raid_event.is_open = True
        self.events_resource.update_raid(self.discord_guild, raid_event)
