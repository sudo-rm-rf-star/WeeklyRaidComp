from commands.raidgroup.RaidGroupCommand import RaidGroupCommand
from client.entities.ShowRaidGroupsMessage import ShowRaidGroupsMessage


class ListRaidGroups(RaidGroupCommand):
    def __init__(self):
        subname = 'list'
        description = 'Toon alle raid groups'
        super(ListRaidGroups, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        await ShowRaidGroupsMessage(self.client, self.discord_guild, self.player, self.guild).send_to(self.member)

