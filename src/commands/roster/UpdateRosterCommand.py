from commands.roster.RosterCommand import RosterCommand
from logic.enums.RosterStatus import RosterStatus
from utils.DateOptionalTime import DateOptionalTime
from exceptions.MissingImplementationException import MissingImplementationException
from exceptions.InvalidArgumentException import InvalidArgumentException


class UpdateRosterCommand(RosterCommand):
    @classmethod
    def roster_choice(cls) -> RosterStatus: raise MissingImplementationException()

    @classmethod
    def argformat(cls) -> str: return "raid_name character [raid_date][raid_time]"

    async def execute(self, raid_name: str, character: str, raid_datetime: DateOptionalTime, **kwargs):
        raid_event = self.get_raid_event(raid_name, raid_datetime)
        # Bugged: we cannot use guild_id...
        player = self.players_resource.get_player_by_name(character, self.guild)
        if not player:
            raise InvalidArgumentException(f"Could not find character {character}")
        updated_character = raid_event.add_to_roster(player, self.roster_choice())
        self.events_resource.update_raid(self.discord_guild, raid_event)
        self.publish_roster_changes([updated_character], raid_event)
        self.respond(f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully updated.')
