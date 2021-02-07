from dokbot.commands.raidteam.RaidTeamCommand import RaidTeamCommand
from dokbot.utils.RaidTeamSelectionInteraction import RaidTeamSelectionInteraction


class SelectRaidTeam(RaidTeamCommand):
    @classmethod
    def sub_name(cls) -> str: return "select"

    @classmethod
    def description(cls) -> str: return "Select an existing raid team you'd like to manage or add a new one."

    async def execute(self, **kwargs) -> None:
        raid_team = await self.interact(RaidTeamSelectionInteraction)
        self.respond(f'You will now manage {raid_team}')
