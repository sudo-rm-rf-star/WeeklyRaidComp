from commands.roster.RosterCommand import RosterCommand
from utils.AttendanceReader import update_raid_presence


class CreateRosterCommand(RosterCommand):
    def __init__(self):
        argformat = "raid_name [raid_date][raid_time]"
        subname = 'create'
        description = 'Maak een raid compositie voor een event'
        super(RosterCommand, self).__init__('roster', subname, description, argformat)

    async def execute(self, raid_name, raid_datetime, **kwargs):
        update_raid_presence(self.players_resource, self.events_resource)
        guild_id, group_id = self.get_guild_id_and_group_id()
        if not group_id:
            return
        raid_event = self.events_resource.get_raid(guild_id, group_id, raid_name, raid_datetime)
        updated_players = raid_event.compose_roster()
        self.events_resource.update_raid(raid_event)
        self.publish_roster_changes(updated_players, raid_event)
        success_indicator = 'successfully' if len(updated_players) > 0 else 'unsuccessfully'
        self.respond(f'Roster for {raid_event.get_name()} on {raid_event.get_datetime()} has been {success_indicator} updated.')
