from dokbot.DokBotCog import DokBotCog


class ShowRaidEvent(DokBotCog):
    @classmethod
    def argformat(cls) -> str:
        return "raid_name [raid_datetime]"

    @classmethod
    def description(cls) -> str:
        return "Posts another message for the given event"

    @classmethod
    def sub_name(cls) -> str:
        return "show"

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event = await self.get_raid_event(raid_name, raid_datetime)
        await self.send_raid_message(self.channel, raid_event)
        self.events_resource.update_raid(self.discord_guild, raid_event)
