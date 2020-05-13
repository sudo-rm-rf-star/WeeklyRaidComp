from commands.roster.RosterCommand import RosterCommand
from client.entities.RaidMessage import RaidMessage
from utils.AttendanceReader import update_raid_presence


class CreateRosterCommand(RosterCommand):
    def __init__(self):
        argformat = "raid_name [raid_date][raid_time]"
        subname = 'create'
        description = 'Maak een raid compositie voor een event'
        super(RosterCommand, self).__init__('roster', subname, description, argformat)

    async def execute(self, raid_name, raid_datetime, **kwargs):
        update_raid_presence(self.players_resource, self.events_resource)
        raid_event = self.events_resource.get_raid(raid_name, raid_datetime)
        updated_players = raid_event.compose_roster()
        RaidMessage(self.client, raid_event).sync()
        success_indicator = 'successfully' if len(updated_players) > 0 else 'unsuccessfully'
        self.publish_roster_changes(updated_players, raid_event)
        self.respond(f'Roster for {raid_event.get_name()} on {raid_event.get_datetime()} has been {success_indicator} updated.')
