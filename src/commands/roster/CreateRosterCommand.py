from commands.roster.RosterCommand import RosterCommand
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
        raid_event: RaidEvent = self.get_raid_event(raid_name, raid_datetime)
        self.respond(f"Starting roster creation for {raid_event}. This might take long running this for the first time")
        updated_characters = raid_event.compose_roster()
        self.events_resource.update_raid(self.discord_guild, raid_event)
        self.publish_roster_changes(updated_characters, raid_event)
        success_indicator = 'successfully' if len(updated_characters) > 0 else 'unsuccessfully'
        self.respond(f'Roster for {raid_event} has been {success_indicator} updated.')
