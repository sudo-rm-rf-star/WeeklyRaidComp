from commands.raid.RaidCommand import RaidCommand
from utils.DiscordUtils import get_member_by_id


class EditRaidEvent(RaidCommand):
    @classmethod
    def argformat(cls) -> str: return "raid_name raid_date raid_time new_raid_name new_raid_date new_raid_time"

    @classmethod
    def description(cls) -> str: return "Edits an existing raid event"

    @classmethod
    def subname(cls) -> str: return "edit"

    async def execute(self, raid_name, raid_datetime, new_raid_name, new_raid_datetime, **kwargs):
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime)
        if not raid_event:
            self.respond(f'Found no raid event for {raid_name} on {raid_datetime}')
            return

        if new_raid_name == raid_event.name and  raid_event.datetime == new_raid_datetime:
            self.respond(f'The new raid equals the old raid, aborting...')
            return

        old_event_str = str(raid_event)
        raid_event.name = new_raid_name
        raid_event.datetime = new_raid_datetime
        self.events_resource.delete_raid(raid_event)
        self.events_resource.update_raid(self.discord_guild, raid_event)
        for character in raid_event.roster.characters:
            member = await get_member_by_id(self.discord_guild, character.discord_id)
            # await member.send(f'An event you signed up was changed from {old_event_str} to {str(raid_event)}.')
