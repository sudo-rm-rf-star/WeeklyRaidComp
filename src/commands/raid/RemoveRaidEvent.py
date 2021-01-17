from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime


class RemoveRaidCommand(RaidCommand):
    @classmethod
    def subname(cls) -> str:
        return "remove"

    @classmethod
    def argformat(cls) -> str:
        return "raid_name [raid_date][raid_time][silent]"

    @classmethod
    def description(cls) -> str:
        return "Remove the event for a raid"

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, silent: bool, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        await self.events_resource.remove_raid(self.discord_guild, raid_event)
        if not silent:
            self.send_message_to_raiders(f'{raid_event} has been cancelled.')
        self.respond(f'{raid_event} has been successfully deleted.')
