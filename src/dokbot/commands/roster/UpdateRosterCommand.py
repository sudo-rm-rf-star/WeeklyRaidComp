from dokbot.commands.roster.RosterCommand import RosterCommand
from logic.enums.RosterStatus import RosterStatus
from exceptions.MissingImplementationException import MissingImplementationException
from exceptions.InvalidInputException import InvalidInputException
from datetime import datetime
from persistence.RaidEventsResource import RaidEventsResource


class UpdateRosterCommand(RosterCommand):
    @classmethod
    def roster_choice(cls) -> RosterStatus: raise MissingImplementationException()

    @classmethod
    def argformat(cls) -> str: return "raid_name character [raid_datetime]"

    async def execute(self, raid_name: str, character: str, raid_datetime: datetime, **kwargs):
        raid_event = await self.get_raid_event(raid_name, raid_datetime)
        player = self.players_resource.get_player_by_name(character, await self.get_raidteam())
        if not player:
            raise InvalidInputException(f"Could not find character {character}")
        updated_character = raid_event.add_to_roster(player, self.roster_choice())
        RaidEventsResource().update_raid(raid_event)
        self.publish_roster_changes([updated_character], raid_event)
        self.respond(f'Raid event for {raid_event.get_name()} on {raid_event.get_datetime()} has been successfully updated.')
