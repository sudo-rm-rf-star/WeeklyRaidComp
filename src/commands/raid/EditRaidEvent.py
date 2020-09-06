from commands.raid.RaidCommand import RaidCommand
from utils.DateOptionalTime import DateOptionalTime


class EditRaidEvent(RaidCommand):
    @classmethod
    def argformat(cls) -> str:
        return "raid_name raid_date raid_time new_raid_name new_raid_date new_raid_time"

    @classmethod
    def description(cls) -> str:
        return "Edits an existing raid event"

    @classmethod
    def subname(cls) -> str:
        return "edit"

    async def execute(self, raid_name, raid_datetime, new_raid_name, new_raid_datetime, **kwargs):
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name,
                                                   raid_datetime)
        if not raid_event:
            self.respond(f'Found no raid event for {raid_name} on {raid_datetime}')
            return

        if new_raid_name == raid_event.name and raid_event.datetime == new_raid_datetime:
            self.respond(f'The new raid equals the old raid, aborting...')
            return

        is_open = raid_event.is_open
        roster = raid_event.roster
        new_raid_event = await self.create_raid(new_raid_name, new_raid_datetime, is_open)
        new_raid_event.roster = roster
        new_raid_event.is_open = is_open
        self.events_resource.update_raid(self.discord_guild, new_raid_event)
        self.events_resource.delete_raid(raid_event)
        if new_raid_event.get_datetime() < DateOptionalTime.now():
            self.send_message_to_raiders(f'An event has been updated from {str(raid_event)} to {str(new_raid_event)}. '
                                         f'If you already signed, you are still signed for the new raid.')
