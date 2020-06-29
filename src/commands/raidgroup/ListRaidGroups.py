from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from client.entities.ShowRaidGroupsMessage import ShowRaidGroupsMessage


class ListRaidGroups(RaidGroupCommand):
    @classmethod
    def subname(cls) -> str: return "list"

    @classmethod
    def description(cls) -> str: return "Show all raid groups in this guild"

    async def execute(self, **kwargs) -> None:
        await ShowRaidGroupsMessage(self.client, self.discord_guild, self.player, self.guild).send_to(self.member)

