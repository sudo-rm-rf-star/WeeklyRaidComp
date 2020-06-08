from commands.roster.RosterCommand import RosterCommand
from utils.Constants import OFFICER_RANK
from logic.enums.RosterStatus import RosterStatus
from client.entities.RaidMessage import RaidMessage
from utils.DateOptionalTime import DateOptionalTime


class UpdateRosterCommand(RosterCommand):
    def __init__(self, subname: str, description: str, roster_choice: RosterStatus):
        argformat = "raid_name player [raid_date][raid_time][team_index]"
        required_rank = OFFICER_RANK
        self.roster_choice = roster_choice
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank)

    async def execute(self, raid_name: str, player: str, raid_datetime: DateOptionalTime, team_index: int, **kwargs):
        guild_id, group_id = self.get_guild_id_and_group_id()
        if not group_id:
            return
        raid_event = self.events_resource.get_raid(guild_id, group_id, raid_name, raid_datetime)
        player = self.players_resource.get_character(player)
        raid_event.add_to_roster(player, self.roster_choice)
        self.events_resource.update_raid(raid_event)
        RaidMessage(self.client, raid_event).sync()
        self.publish_roster_changes([player], raid_event)
        self.respond(f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully updated.')
