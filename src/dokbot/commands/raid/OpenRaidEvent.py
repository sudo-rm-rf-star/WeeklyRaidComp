from dokbot.commands.raid.RaidCog import RaidCog


class OpenRaidEvent(RaidCog):
    @classmethod
    def sub_name(cls) -> str: return "open"

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_datetime]"

    @classmethod
    def description(cls) -> str: return "Opens an event so that anyone can join. This will add signup buttons to the event message."

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = await self.get_raid_event(raid_name, raid_datetime)
        raid_event.is_open = True
        self.raids_resource.update_raid(self.discord_guild, raid_event)
