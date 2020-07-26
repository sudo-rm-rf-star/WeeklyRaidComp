from commands.roster.RosterCommand import RosterCommand
from utils.AttendanceReader import update_raid_presence


class CreateRosterCommand(RosterCommand):
    @classmethod
    def subname(cls) -> str: return "create"

    @classmethod
    def description(cls) -> str: return "Create a roster for a raid event. This command can be used several times for the same event."

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_date][raid_time]"

    async def execute(self, raid_name, raid_datetime, **kwargs):
        update_raid_presence(self.discord_guild.id, self.get_raidgroup().group_id, self.guild.wl_guild_id, self.events_resource, self.players_resource)
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime)
        updated_characters = raid_event.compose_roster()
        self.events_resource.update_raid(self.discord_guild, raid_event)
        self.publish_roster_changes(updated_characters, raid_event)
        success_indicator = 'successfully' if len(updated_characters) > 0 else 'unsuccessfully'
        self.respond(f'Roster for {raid_event.get_name()} on {raid_event.get_datetime()} has been {success_indicator} updated.')
