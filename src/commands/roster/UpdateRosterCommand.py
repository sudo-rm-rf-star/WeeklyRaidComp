from commands.roster.RosterCommand import RosterCommand
from logic.enums.RosterStatus import RosterStatus
from client.entities.RaidMessage import RaidMessage
from utils.DateOptionalTime import DateOptionalTime
from exceptions.MissingImplementationException import MissingImplementationException


class UpdateRosterCommand(RosterCommand):
    @classmethod
    def roster_choice(cls) -> RosterStatus: raise MissingImplementationException()

    @classmethod
    def argformat(cls) -> str: return "raid_name player [raid_date][raid_time]"

    async def execute(self, raid_name: str, player: str, raid_datetime: DateOptionalTime, **kwargs):
        raid_event = self.events_resource.get_raid(self.discord_guild, self.get_raidgroup().group_id, raid_name, raid_datetime)
        player = self.players_resource.get_player_by_name(player, self.discord_guild.id)
        raid_event.add_to_roster(player, UpdateRosterCommand.roster_choice())
        self.events_resource.update_raid(self.discord_guild, raid_event)
        RaidMessage(self.client, self.discord_guild, raid_event).sync()
        await self.publish_roster_changes([player.get_selected_char()], raid_event)
        self.respond(f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully updated.')
