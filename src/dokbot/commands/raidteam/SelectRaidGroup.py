from dokbot.commands.raidteam.RaidTeamCommand import RaidTeamCommand
from dokbot.utils.RaidTeamSelectionInteraction import RaidTeamSelectionInteraction


class SelectRaidTeam(RaidTeamCommand):
    @classmethod
    def sub_name(cls) -> str: return "select"

    @classmethod
    def argformat(cls) -> str: return "raidteam"

    @classmethod
    def description(cls) -> str: return "Select an existing raid team you'd like to manage or add a new one."

    async def execute(self, **kwargs) -> None:
        return await self.interact(RaidTeamSelectionInteraction)
