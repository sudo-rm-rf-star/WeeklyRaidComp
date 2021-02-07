from dokbot.commands.roster.RosterCommand import RosterCommand
from persistence.RaidEventsResource import RaidEventsResource
from logic.RaidEvent import RaidEvent


class CreateRosterCommand(RosterCommand):
    @classmethod
    def sub_name(cls) -> str: return "create"

    @classmethod
    def description(cls) -> str: return "Create a roster for a raid event. " \
                                        "This command can be used several times for the same event."

    @classmethod
    def argformat(cls) -> str: return "raid_name [raid_datetime]"

    async def execute(self, raid_name, raid_datetime, **kwargs):
        raid_event: RaidEvent = await self.get_raid_event(raid_name, raid_datetime)
        self.respond(f"Starting roster creation for {raid_event}. This might take long running this for the first time")
        updated_characters = raid_event.compose_roster()
        RaidEventsResource().update_raid(raid_event)
        self.publish_roster_changes(updated_characters, raid_event)
        self.respond(f'Roster for {raid_event} has been successfully updated. There were {len(updated_characters)} changes')
