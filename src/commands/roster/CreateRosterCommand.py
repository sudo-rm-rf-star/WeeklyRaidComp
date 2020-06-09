from commands.roster.RosterCommand import RosterCommand
from utils.AttendanceReader import update_raid_presence


class CreateRosterCommand(RosterCommand):
    def __init__(self):
        argformat = "raid_name [raid_date][raid_time]"
        subname = 'create'
        description = 'Maak een raid compositie voor een event'
        super(RosterCommand, self).__init__(name='roster', subname=subname, description=description, argformat=argformat)

    async def execute(self, raid_name, raid_datetime, **kwargs):
        update_raid_presence(self.players_resource, self.events_resource)
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime)
        updated_players = raid_event.compose_roster()
        self.events_resource.update_raid(self.discord_guild, raid_event)
        self.publish_roster_changes(updated_players, raid_event)
        success_indicator = 'successfully' if len(updated_players) > 0 else 'unsuccessfully'
        self.respond(f'Roster for {raid_event.get_name()} on {raid_event.get_datetime()} has been {success_indicator} updated.')
