from commands.roster.RosterCommand import RosterCommand
from logic.enums.RosterStatus import RosterStatus
from client.entities.RaidMessage import RaidMessage
from utils.DateOptionalTime import DateOptionalTime


class UpdateRosterCommand(RosterCommand):
    def __init__(self, *, subname: str, description: str, roster_choice: RosterStatus):
        argformat = "raid_name player [raid_date][raid_time][team_index]"
        self.roster_choice = roster_choice
        super(RosterCommand, self).__init__(name='roster', subname=subname, description=description, argformat=argformat)

    async def execute(self, raid_name: str, player: str, raid_datetime: DateOptionalTime, team_index: int, **kwargs):
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime)
        player = self.players_resource.get_player_by_name(player, self.discord_guild.id)
        raid_event.add_to_roster(player, self.roster_choice)
        self.events_resource.update_raid(self.discord_guild, raid_event)
        RaidMessage(self.client, self.discord_guild, raid_event).sync()
        self.publish_roster_changes([player.get_selected_char()], raid_event)
        self.respond(f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully updated.')
