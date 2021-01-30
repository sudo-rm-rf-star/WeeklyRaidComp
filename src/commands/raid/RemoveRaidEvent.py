from commands.raid.RaidCommand import RaidCommand
from datetime import datetime


class RemoveRaidCommand(RaidCommand):
    @classmethod
    def sub_name(cls) -> str:
        return "remove"

    @classmethod
    def argformat(cls) -> str:
        return "raid_name [raid_datetime][silent]"

    @classmethod
    def description(cls) -> str:
        return "Remove the event for a raid"

    async def execute(self, raid_name: str, raid_datetime: datetime, silent: bool, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        await self.events_resource.remove_raid(self.discord_guild, raid_event)
        if not silent:
            self.send_message_to_raiders(f'{raid_event} has been cancelled.')
        self.respond(f'{raid_event} has been successfully deleted.')
