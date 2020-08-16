from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime
from utils.DiscordUtils import get_member_by_id


class RemoveRaidCommand(RaidCommand):
    @classmethod
    def subname(cls) -> str:
        return "remove"

    @classmethod
    def argformat(cls) -> str:
        return "raid_name [raid_date][raid_time]"

    @classmethod
    def description(cls) -> str:
        return "Remove the event for a raid"

    async def execute(self, raid_name: str, raid_datetime: DateOptionalTime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        await self.events_resource.remove_raid(self.discord_guild, raid_event)
        for player in raid_event.get_signed_characters():
            member = await get_member_by_id(self.discord_guild, player.discord_id)
            if member is not None:
                member.send(f'{raid_event} has been cancelled. Thanks for signing up!')

        self.respond(f'{raid_event} has been successfully deleted.')
